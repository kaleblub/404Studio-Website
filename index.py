from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    # port = int(os.getenv("PORT", 5000))  # Vercel uses PORT env variable
    # app.run(debug=True, host="0.0.0.0", port=port)