import os
import shutil
import json
import pandas as pd

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from langchain.text_splitter import CharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import CSVLoader, UnstructuredExcelLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

from .models import UploadedFile, NlpQuery
from .serializers import UploadedFileSerializer, NlpQuerySerializer


class UploadedFileViewSet(ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new instance of the `UploadedFile` model based on the provided data.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response containing the serialized data and the table in JSON format if the file is valid,
                      or the serializer errors if the file is not valid.

        Notes:
            - The function first checks if the provided data is valid by using the serializer.
            - If the data is valid, it retrieves the file from the serializer's validated data.
            - It then checks if the file's content type is one of the allowed content types. If not, it returns a 400
              Bad Request response with an error message.
            - If the file's content type is "text/csv", it reads the file using `pd.read_csv()`. Otherwise, it reads the
              file using `pd.read_excel()` with the "openpyxl" engine.
            - It then converts the DataFrame to JSON format with the "records" orientation.
            - Finally, it saves the serializer and returns a 201 Created response with the serialized data and the table
              in JSON format.

        """
        request.data["content_type"] = request.data["file"].content_type
        serializer = self.serializer_class(data=request.data)

        allowed_content_types = [
            "text/csv",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel",
        ]

        if serializer.is_valid():
            file = serializer.validated_data["file"]

            # Check if the file content type is allowed
            if file.content_type not in allowed_content_types:
                return Response(
                    {
                        "status": 400,
                        "message": "Unsupported file type. Please upload a CSV or Excel file.",
                        "data": None,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Read the file and convert it to JSON
            df = (
                pd.read_csv(file)
                if file.content_type == "text/csv"
                else pd.read_excel(file, engine="openpyxl")
            )
            json_data = df.to_json(orient="records")

            serializer.save()

            return Response(
                {
                    "status": 200,
                    "message": "File uploaded successfully.",
                    "data": {"serializer": serializer.data, "table": json_data},
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "status": 400,
                "message": "Invalid file. Please upload a CSV or Excel file.",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def perform_destroy(self, serializer):
        """
        Deletes a file associated with the given serializer and removes it from the file system.

        Parameters:
            serializer (Serializer): The serializer object containing the file to be deleted.

        Returns:
            None
        """
        serializer.delete()


class NlpQueryViewSet(ModelViewSet):
    queryset = NlpQuery.objects.all()
    serializer_class = NlpQuerySerializer

    def create(self, request, *args, **kwargs):
        """
        Creates a new NLP query based on the provided request data.

        Parameters:
            request (HttpRequest): The HTTP request object containing the data for the new query.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object containing the result of the query.

        Raises:
            ValidationError: If the serializer is not valid.

        Description:
            This function creates a new NLP query based on the provided request data. It first validates the serializer
            using the provided request data. If the serializer is valid, it retrieves the last uploaded file from the
            database and gets its path on the file system. It then sets the embedding model to use. If the "same_file"
            flag in the serializer data is True, it loads the previous vector store. Otherwise, it creates a loader
            based on the file content type and loads the documents. The documents are then split into smaller chunks
            and a Chroma vector store is created using the documents and the embedding model. The user query is then
            retrieved from the serializer data and used to retrieve relevant documents from the vector store. The relevant
            documents are combined with the query to create a combined input for the ChatOpenAI model. The model is
            invoked with the combined input and the result is parsed to extract the regex pattern and replacement
            value. The original file is then read using the appropriate loader based on its content type. If a replacement
            value is provided, the data is transformed using the regex pattern and replacement value. The transformed
            data is then converted to JSON format and returned in the HTTP response. If the serializer is not valid,
            a 400 Bad Request response is returned with the serializer errors.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Get the file path
            file = UploadedFile.objects.last()
            file_on_disk = FileSystemStorage().path(file.file.name)

            # Set embedding model
            embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

            if serializer.validated_data["same_file"]:
                # Load previous vector store
                db = Chroma(
                    persist_directory=str(settings.CHROMA_DIR),
                    embedding_function=embedding,
                )
            else:
                # Create the loader based on the file content type
                loader = (
                    CSVLoader(file_on_disk)
                    if file.content_type == "text/csv"
                    else UnstructuredExcelLoader(file_on_disk)
                )
                documents = loader.load()

                # Split the documents into smaller chunks
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                docs = text_splitter.split_documents(documents)

                # Display information about the split documents
                print("\n--- Document Chunks Information ---")
                print(f"Number of document chunks: {len(docs)}")
                print(f"Sample chunk:\n{docs[0].page_content}\n")

                # Recreate store
                chroma_dir = str(settings.CHROMA_DIR)
                shutil.rmtree(chroma_dir, ignore_errors=False)
                db = Chroma.from_documents(
                    docs, embedding, persist_directory=chroma_dir
                )

            # Get user query
            query = serializer.validated_data["query"]

            # Retrieve relevant documents based on the query
            retriever = db.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 1},
            )
            relevant_docs = retriever.invoke(query)

            # Combine the query and the relevant documents
            combined_input = (
                "Here are some documents that might help answer the question: "
                + query
                + "\n\nRelevant Documents:\n"
                + "\n\n".join([doc.page_content for doc in relevant_docs])
                + "\n\nPlease provide an answer in the form json in the following format."
                + '\n\n{"regex": "regex pattern", "replacement": "replacement result"}'
                + '\n\nIf the answer is not found in the documents, respond with {"regex": "", "replacement": ""}'
                + '\n\nIf the user does not provide a replacement value, respond with {"regex": "regex result", "replacement": ""}.'
            )

            # Create a ChatOpenAI model
            llm_model = ChatOpenAI(model="gpt-4o-mini")

            # Define the messages for the model
            llm_messages = [
                SystemMessage(
                    content="You are a regex pattern finder. User might also provide a replacement value."
                    + "\n\nFind the pattern and pass the replacement value to end result"
                ),
                HumanMessage(content=combined_input),
            ]

            # Invoke the model with the combined input
            llm_result = llm_model.invoke(llm_messages)

            json_llm_result = json.loads(llm_result.content)
            regex = json_llm_result["regex"]
            replacement = json_llm_result["replacement"]

            df = (
                pd.read_csv(file_on_disk)
                if file.content_type == "text/csv"
                else pd.read_excel(file_on_disk, engine="openpyxl")
            )

            # Transform the data
            if replacement:
                df = df.replace(regex, replacement, regex=True)

            json_data = df.to_json(orient="records")

            return Response(
                {
                    "status": 200,
                    "message": "Processed query successfully.",
                    "data": {
                        "serializer": serializer.data,
                        "table": json_data,
                        "pattern": regex,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "status": 400,
                "message": "NLP queries cannot be created directly.",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
