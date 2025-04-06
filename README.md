# FitBro

FitBro is a health recommendation system powered by Google Gemini and LangChain, delivering tailored diet and workout plans based on your age, gender, height, weight, region, dietary preferences, allergies, and health conditions. Achieve your wellness goals with ease!

## Features

- **Custom Plans**: Get diet and workout recommendations tailored to your unique profile.  
- **AI-Driven Insights**: Leverages Google Gemini for accurate and detailed suggestions.  
- **Simple Interface**: User-friendly design for seamless interaction.

## Technologies

- **Streamlit**: Python framework for building the web app.  
- **Google Gemini API**: Provides advanced AI capabilities for recommendations.  
- **LangChain**: Facilitates interaction with the Gemini API.

## Setup

1. **Get a Google Gemini API Key**: Obtain your API key from Google.  
2. **Clone the Repository**:  
   ```bash
   git clone https://github.com/msaadg/fitbro.git
   cd fitbro
   ```  
3. **Install Dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```  
4. **Set Up API Key**: Create a `.env` file and add:  
   ```env
   GOOGLE_API_KEY=your_gemini_api_key
   ```  
5. **Run the App**:  
   ```bash
   streamlit run app.py
   ```

## Contributing

1. Fork the repository.  
2. Create a branch (`git checkout -b feature-branch`).  
3. Commit changes (`git commit -m 'Add feature'`).  
4. Push (`git push origin feature-branch`).  
5. Open a pull request.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contact

Developed by Muhammad Saad  
- LinkedIn: [Muhammad Saad](https://www.linkedin.com/in/msaad01)  
- GitHub: [msaadg](https://github.com/msaadg)