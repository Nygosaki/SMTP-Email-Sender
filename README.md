# Email Sender Tool

## Overview

This Python script allows you to send emails using the Simple Mail Transfer Protocol (SMTP). It is configured through a `.env` file, providing flexibility in setting up various email parameters.

## Prerequisites

1. **Python**: Ensure you have Python installed on your machine.
2. **Dependencies**: Install the required dependencies using the following command:
   ```bash
   pip install python-dotenv
   pip install dnspython
   ```

## Setup

1. Clone the repository to your local machine.
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - For Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - For macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

## Configuration

1. Create a `.env` file in the root directory with the following content:
   ```env
   SMTPSERVER="your_smtp_server"
   SMTPSERVERPORT="your_smtp_port"
   SMTPSERVERUSER="your_smtp_user"
   SMTPSERVERTOKEN="your_smtp_token"
   SENDER="your_sender_email"
   SENDERNAME="your_sender_name"
   RECIEVER="your_receiver_email"
   SUBJECT="your_email_subject"
   CONTENT="your_email_content"
   ```
   Replace the placeholder values with your actual SMTP server details, email addresses, and other parameters.     
   This is not neccesary, though without it, you will be asked to reenter the details every time.     
   The SMTP variables are treated seperately from the others, meaning you can chose to preset only the SMTP variables, and manually enter the per-email details every time.

## Usage

1. Run the script:
   ```bash
   python main.py
   ```
2. If the script detects a `.env` file, it will load the configurations. Otherwise, it will prompt you to enter the necessary details.

3. The script will attempt to send the email, and you will receive a confirmation message if successful.

## Error Handling

- If an error occurs during execution, the script will display an error message indicating the issue.

## Note

- Ensure that your SMTP server allows the specified sender to send emails.

Feel free to customize the email content and subject in the `.env` file according to your needs.
