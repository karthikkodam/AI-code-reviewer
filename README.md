### AI Code Reviewer :
* AI Code Reviewer is a Streamlit-based application that analyzes and reviews submitted code.
* It detects errors, explains them, and suggests fixes. If no issues are found, it provides a brief explanation of what the code does.
* The project utilizes Google Generative AI (Gemini) to generate responses.

### Features :

* Detects errors and bugs in submitted code.
* Provides explanations for detected issues.
* Suggests corrected versions of the code in a copyable format.
* Briefly explains the functionality of error-free code.
* Maintains a history of code reviews for easy reference.


### Prerequisites :

* Ensure you have the following installed:
* Python 3.8+
* pip
* A Google Generative AI API key (stored in API_key.txt)

### Steps :

#### Clone the repository :
git clone : https://github.com/karthikkodam/AI-code-reviewer.git
cd ai-code-reviewer

#### Install dependencies :
pip install -r requirements.txt

####  Add your API key :
Create a file named API_key.txt in the project directory.
Paste your Google Generative AI API key inside the file.

#### Run the application :
streamlit run app.py

### Usage :

* Enter or paste your code into the text area.
* Click the Submit button.
* The AI will analyze the code and provide feedback.
*  Review past submissions in the sidebar.
