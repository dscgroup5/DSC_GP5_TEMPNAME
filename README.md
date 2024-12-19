### Project Setup and Usage Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/dscgroup5/DSC_GP5_TEMPNAME
   cd DSC_GP5_TEMPNAME
   ```

2. **Set API Keys**:
   - Ensure you have valid API keys for Hugging Face and Google Generative AI.
   - Add the following environment variables to your system:
     - `HF_API_KEY`: Your Hugging Face API key.
     - `GOOGLE_API_KEY`: Your Google Generative AI API key.

   #### Setting Environment Variables:
   - **Linux/Mac**:
     ```bash
     export HF_API_KEY="your_hugging_face_api_key"
     export GOOGLE_API_KEY="your_google_api_key"
     ```
   - **Windows** (Command Prompt):
     ```cmd
     set HF_API_KEY=your_hugging_face_api_key
     set GOOGLE_API_KEY=your_google_api_key
     ```
   - Alternatively, create a `.env` file in the project root with the following content:
     ```plaintext
     HF_API_KEY=your_hugging_face_api_key
     GOOGLE_API_KEY=your_google_api_key
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application:

1. **Run the Streamlit App**:
   ```bash
   streamlit run "path_to(app.py)"
   ```

2. **Access the Application**:
   Open your browser and go to `http://localhost:8501` to interact with the app.

