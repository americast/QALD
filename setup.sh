sudo pip3 install -r req.txt
sudo python3 -m spacy download en
python3 -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words')"
mkdir -p data

