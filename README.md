# 🎅 **Secret Santa Generator**  

## **Description**  
The **Secret Santa Generator** is a Python-based web application that organizes Secret Santa events. It randomly pairs participants, generates thoughtful gift recommendations using OpenAI's GPT API, and sends personalized emails via the Gmail API.  

A **live demonstration** is available on [**Hugging Face Spaces**](https://huggingface.co/spaces/galudSla/secret-santa), so you can test the tool without local setup!  

---

## 🚀 **Features**  
- **Randomized Pairing**: Ensures fair and unique gift pairings without duplicates.  
- **Gift Recommendations**: Uses OpenAI's GPT API to suggest personalized gifts based on optional participant input.  
- **Email Automation**: Sends participant details, gift assignments, and recommendations via Gmail API.  
- **Interactive UI**: Powered by Gradio for seamless user interaction.  
- **Live Demo**: Hosted on Hugging Face Spaces for immediate testing.  

---

## 🛠️ **Tech Stack**  
- **Python**  
- **Gradio** (UI Framework)  
- **Gmail API** (Email Automation)  
- **OpenAI GPT API** (Gift Recommendations)  
- **OAuth2** (Gmail API Authentication)  
- **Hugging Face Spaces** (Demo Hosting)  

---

## ⚙️ **Setup Instructions**

### 1. **Prerequisites**  
Ensure you have the following tools installed:  
- Python 3.8+  
- Pip (Python Package Manager)  
- **Google Cloud Platform (GCP)** access for Gmail API setup.  
- **OpenAI API Key**  

---

### 2. **Clone the Repository**  
Run the following command:  
```bash
git clone https://github.com/yourusername/secret-santa-generator.git
cd secret-santa-generator
```

---

### 3. **Set Up Gmail API**  
Before running the app, you must configure the **Gmail API**:  
1. Go to the [Google Developer Console](https://console.cloud.google.com/).  
2. Enable the **Gmail API** for your project.  
3. Generate OAuth 2.0 credentials and download the `credentials.json` file.  
4. Place `credentials.json` in the root directory of the project.  

---

### 4. **Install Dependencies**  
Run the following command to install required libraries:  
```bash
pip install -r requirements.txt
```

---

### 5. **Authenticate Gmail API**  
To authenticate Gmail API and generate your token:  
1. Run the `functions.py` script:  
   ```bash
   python functions.py
   ```
2. Follow the OAuth instructions to allow access.  
3. This creates a `token.json` file.  

---

**6. Configure Environment Variables**  
You need to configure the following environment variables (or use files as described):

- **OpenAI API Key** (required as an environment variable):
  - `OPENAI_API_KEY=your_openai_api_key`  

- **Your Gmail app email** (optional as an environment variable):
  - `app_email=your_email@gmail.com`  

- **Token** (choose one of the following methods):
  - **Option 1: Use `token.json` for persistent storage**  
    If you have already authenticated with the Gmail API and generated a `token.json` file, place the `token.json` file in the root directory. The application will automatically use it.  
    Example code:  
    ```python
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        raise FileNotFoundError("Token file not found. Please authenticate first.")
    ```
  
  - **Option 2: Use environment variables for token management**  
    If you prefer environment-based token management, you can store the token details as a JSON string in an environment variable named `token`.  
    Example code:  
    ```python
    creds = None  
    if 'token' in os.environ:
        token = json.loads(os.getenv('token'))
        creds = Credentials.from_authorized_user_info(token, SCOPES)
    ```
    In this case, there is **no need** for a `token.json` file. Simply set the token environment variable.

---

### Additional Notes:

- **OpenAI API Key**:  
  If your OpenAI API key is set as an environment variable named `OPENAI_API_KEY`, the client will automatically use it. If you have named the environment variable differently, use the code below to fetch the key:  
  ```python
  api_key = os.getenv('API_KEY_something_else')
  ```

- **Hardcoding the OpenAI API Key**:  
  If you prefer to hardcode the API key (not recommended for security reasons), you can uncomment the line below and provide the key directly:  
  ```python
  api_key = "your_openai_api_key"
  ```
  
---

### 7. **Run the Application**  
To launch the Gradio-based app locally, run:  
```bash
python your_script_name.py
```
Open your browser and visit:  
```plaintext
http://localhost:7860
```

---

## 🎥 **How to Use**  
1. Start the app or access the [**Hugging Face Spaces Demo**]((https://huggingface.co/spaces/galudSla/secret-santa)).  
2. Enter participant details, including:  
   - **Name**  
   - **Email**  
   - Optional **gift prompt** (interests or hobbies).  
3. Click **START SECRET SANTA**.  
4. Participants receive emails with:  
   - Their gift recipient's name.  
   - A list of thoughtful gift suggestions generated by ChatGPT.  

---

## 🔑 **Key Implementation Notes**  

### **Difference Between `Credentials.from_authorized_user_info` and `Credentials.from_authorized_user_file`**  
- `Credentials.from_authorized_user_file`:  
   - Loads credentials directly from a `token.json` file saved after OAuth authentication.  
   - Used for persistent storage across sessions.  
   - **Example**:  
     ```python
     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
     ```  
- `Credentials.from_authorized_user_info`:  
   - Loads credentials dynamically from a dictionary or environment variables.  
   - Ideal for deployment scenarios where credentials are stored securely in environment variables.  
   - **Example**:  
     ```python
     creds = Credentials.from_authorized_user_info(token_dict, SCOPES)
     ```  

---

## 🧪 **Testing**  
- Use test email credentials or disable email-sending features temporarily during development.  
- Ensure your Gmail API quota allows sufficient email dispatches.  

---

## 🙌 **Contributing**  
Pull requests are welcome! To contribute:  
1. Fork the repository.  
2. Create a feature branch.  
3. Submit a pull request with a detailed description of your changes.  

---

## 📜 **License**  
This project is licensed under the MIT License.  
