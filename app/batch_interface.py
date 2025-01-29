import streamlit as st
from api_utils import get_api_response
import os
from pathlib import Path
import re
from datetime import datetime
import time
from datetime import datetime, timedelta

def format_time_duration(seconds):
    # Convert seconds to a readable format
    duration = timedelta(seconds=seconds)
    if duration.total_seconds() < 60:
        return f"{duration.total_seconds():.2f} seconds"
    else:
        minutes = duration.total_seconds() / 60
        return f"{minutes:.2f} minutes"

def sanitize_filename(model_name):
    # Format proper filename if original name is ridiculous
    sanitized = re.sub(r'[<>:"/\\|?*]', '', model_name)
    sanitized = re.sub(r'\s+', '_', sanitized)

    sanitized = sanitized[:50]
    sanitized = sanitized.strip('. ')

    if not sanitized:
        sanitized = "UnknownModel"

    return sanitized

def get_safe_filename(model_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    safe_model_name = sanitize_filename(model_name)
    return f"Test-Results-{safe_model_name}-{timestamp}.txt"

def clean_response(response):
    common_prefixes = [
        "According to the provided context,",
        "Based on the provided context,",
        "According to the context,",
        "Based on the context,",
        "From the provided context,"
    ]

    answer = response['answer']
    for prefix in common_prefixes:
        if answer.startswith(prefix):
            answer = answer[len(prefix):].lstrip()

    # Capitalize the first letter if needed
    if answer:
        answer = answer[0].upper() + answer[1:]

    response['answer'] = answer
    return response

def process_batch_questions(file):
    try:
        start_time = time.time()  # Start timing
        questions = [line.decode('utf-8').strip() for line in file.readlines() if line.decode('utf-8').strip()]

        if not questions:
            st.error("The uploaded file is empty or contains no valid questions.")
            return

        results_container = st.container()
        responses = []  # Store responses for later use

        with results_container:
            st.write("### Batch Processing Results")

            # Process questions and store responses
            for i, question in enumerate(questions, 1):
                with st.expander(f"Question {i}: {question}"):
                    with st.spinner(f"Processing question {i}/{len(questions)}..."):
                        try:
                            response = get_api_response(
                                question=question,
                                session_id=None,
                                model=st.session_state["model"]
                            )
                            responses.append((question, response))

                            if response:
                                st.write("**Answer:**")
                                st.write(response['answer'])
                                st.write("---")
                                st.write("**Model Used:**", response['model'])
                            else:
                                st.error(f"Failed to get response for question: {question}")
                        except Exception as e:
                            st.error(f"Error processing question {i}: {str(e)}")
                            responses.append((question, None))

        # Calculate total processing time
        end_time = time.time()
        processing_time = end_time - start_time
        formatted_time = format_time_duration(processing_time)

        # Display processing time in the UI
        st.write(f"### Processing Complete")
        st.write(f"Total processing time: {formatted_time}")
        st.write(f"Average time per question: {format_time_duration(processing_time/len(questions))}")

        # Create download section
        st.write("### Download Results")

        # Create formatted results string with processing information
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results_text = f"""Batch Processing Results
Generated: {timestamp}
Model Used: {st.session_state['model']}
Number of Questions: {len(questions)}
Total Processing Time: {formatted_time}
Average Time per Question: {format_time_duration(processing_time/len(questions))}

===========================================

"""
        # Add individual results
        for i, (question, response) in enumerate(responses, 1):
            results_text += f"Question {i}: {question}\n"
            if response:
                results_text += f"Answer: {response['answer']}\n"
                results_text += f"Model: {response['model']}\n"
            else:
                results_text += "Error: Failed to get response\n"
            results_text += "\n---\n\n"

        # Provide download button
        filename = get_safe_filename(st.session_state["model"])
        download_clicked = st.download_button(
            label="Download Results as Text",
            data=results_text,
            file_name=filename,
            mime="text/plain",
            key="download_button"
        )

        if download_clicked:
            st.success("File has been downloaded! Check your browser's default download location.")

        # Add restart button
        if st.button("Start New Batch"):
            st.session_state.clear()
            st.rerun()

    except UnicodeDecodeError:
        st.error("Error: The uploaded file is not properly formatted as UTF-8 text.")
    except Exception as e:
        st.error(f"An unexpected error occurred while processing the file: {str(e)}")

def display_batch_interface():
    st.write("## Batch Question Processing")
    st.write("Upload a text file with one question per line to process them in batch.")

    uploaded_file = st.file_uploader("Choose a text file", type=["txt"])

    if uploaded_file is not None:
        if st.button("Process Questions"):
            process_batch_questions(uploaded_file)
