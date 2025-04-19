import os
import json
import pandas as pd
from typing import List, Dict, Any
import random


def preprocess_data(raw_data_path: str, output_path: str) -> None:
    """
    Preprocess raw data into Q&A format.

    Args:
        raw_data_path: Path to raw data files
        output_path: Path to save processed data
    """
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Process different data formats
    processed_data = []

    # Walk through the raw data directory
    for root, dirs, files in os.walk(raw_data_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Process based on file extension
            if file.endswith('.csv'):
                data = _process_csv(file_path)
            elif file.endswith('.json'):
                data = _process_json(file_path)
            elif file.endswith('.txt'):
                data = _process_txt(file_path)
            else:
                continue

            processed_data.extend(data)

    # Save processed data
    with open(os.path.join(output_path, 'qa_data.json'), 'w') as f:
        json.dump(processed_data, f, indent=2)

    print(f"Processed {len(processed_data)} Q&A pairs.")


def _process_csv(file_path: str) -> List[Dict[str, str]]:
    """Process a CSV file into Q&A pairs."""
    try:
        df = pd.read_csv(file_path)

        # Assume the CSV has 'question' and 'answer' columns
        # Adjust column names as needed for your data
        if 'question' in df.columns and 'answer' in df.columns:
            qa_pairs = []
            for _, row in df.iterrows():
                qa_pairs.append({
                    'question': row['question'],
                    'answer': row['answer']
                })
            return qa_pairs
        else:
            print(f"CSV file {file_path} does not have required columns.")
            return []
    except Exception as e:
        print(f"Error processing CSV file {file_path}: {e}")
        return []


def _process_json(file_path: str) -> List[Dict[str, str]]:
    """Process a JSON file into Q&A pairs."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        qa_pairs = []

        # Handle different JSON formats
        if isinstance(data, list):
            for item in data:
                if 'question' in item and 'answer' in item:
                    qa_pairs.append({
                        'question': item['question'],
                        'answer': item['answer']
                    })
        elif isinstance(data, dict):
            # Handle conversational format
            if 'conversations' in data:
                for conv in data['conversations']:
                    if 'messages' in conv:
                        messages = conv['messages']
                        for i in range(0, len(messages) - 1, 2):
                            if i + 1 < len(messages):
                                qa_pairs.append({
                                    'question': messages[i]['content'],
                                    'answer': messages[i + 1]['content']
                                })

        return qa_pairs
    except Exception as e:
        print(f"Error processing JSON file {file_path}: {e}")
        return []


def _process_txt(file_path: str) -> List[Dict[str, str]]:
    """Process a text file into Q&A pairs."""
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        qa_pairs = []
        current_question = None
        current_answer = []

        for line in lines:
            line = line.strip()
            if not line:
                # Empty line marks end of a Q&A pair
                if current_question and current_answer:
                    qa_pairs.append({
                        'question': current_question,
                        'answer': '\n'.join(current_answer)
                    })
                    current_question = None
                    current_answer = []
            elif line.startswith('Q:') or line.startswith('Question:'):
                # Start of a new question
                if current_question and current_answer:
                    qa_pairs.append({
                        'question': current_question,
                        'answer': '\n'.join(current_answer)
                    })
                current_question = line.split(':', 1)[1].strip()
                current_answer = []
            elif line.startswith('A:') or line.startswith('Answer:'):
                # Start of an answer
                current_answer.append(line.split(':', 1)[1].strip())
            elif current_question is not None:
                # Continuation of current answer
                current_answer.append(line)

        # Add the last Q&A pair if it exists
        if current_question and current_answer:
            qa_pairs.append({
                'question': current_question,
                'answer': '\n'.join(current_answer)
            })

        return qa_pairs
    except Exception as e:
        print(f"Error processing text file {file_path}: {e}")
        return []


def split_data(data_path: str, train_ratio: float = 0.8) -> Dict[str, List[Dict[str, str]]]:
    """
    Split data into training and validation sets.

    Args:
        data_path: Path to processed data
        train_ratio: Ratio of data to use for training

    Returns:
        Dictionary with 'train' and 'val' datasets
    """
    try:
        # Load processed data
        with open(os.path.join(data_path, 'qa_data.json'), 'r') as f:
            data = json.load(f)

        # Shuffle data
        random.shuffle(data)

        # Split data
        split_idx = int(len(data) * train_ratio)
        train_data = data[:split_idx]
        val_data = data[split_idx:]

        # Save splits
        with open(os.path.join(data_path, 'train_data.json'), 'w') as f:
            json.dump(train_data, f, indent=2)

        with open(os.path.join(data_path, 'val_data.json'), 'w') as f:
            json.dump(val_data, f, indent=2)

        return {
            'train': train_data,
            'val': val_data
        }
    except Exception as e:
        print(f"Error splitting data: {e}")
        return {'train': [], 'val': []}


def convert_to_openai_format(qa_data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Convert Q&A data to OpenAI API format.

    Args:
        qa_data: List of Q&A pairs

    Returns:
        Data in OpenAI format
    """
    openai_format = []

    for qa_pair in qa_data:
        openai_format.append({
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": qa_pair["question"]},
                {"role": "assistant", "content": qa_pair["answer"]}
            ]
        })

    return openai_format


def main() -> None:
    """Main function to run the training pipeline."""
    # Paths
    raw_data_path = "data/raw"
    processed_data_path = "data/processed"

    # Preprocess data
    preprocess_data(raw_data_path, processed_data_path)

    # Split data
    data_splits = split_data(processed_data_path)

    print(f"Training data: {len(data_splits['train'])} examples")
    print(f"Validation data: {len(data_splits['val'])} examples")

    # Convert to OpenAI format (for reference)
    train_openai = convert_to_openai_format(data_splits['train'])
    with open(os.path.join(processed_data_path, 'train_openai_format.json'), 'w') as f:
        json.dump(train_openai, f, indent=2)


if __name__ == "__main__":
    main()