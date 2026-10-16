# 🧬 DNA Storage Lab

### Multimedia Storage Using DNA Encoding

DNA Storage Lab is an interactive Python application that simulates
digital data storage using DNA sequences.

The application converts text, images, and videos into simulated
DNA sequences and demonstrates data recovery, mutation simulation,
integrity verification, and error correction.

## ✨ Features

- 📝 Text-to-DNA encoding and decoding
- 🖼️ Image-to-DNA encoding and reconstruction
- 🎥 Video-to-DNA encoding and reconstruction
- 🧬 Binary-to-DNA mapping using A, C, G, and T
- 🔐 SHA-256 integrity verification
- 🧪 Random DNA mutation simulation
- 🛡️ Reed–Solomon error correction
- 📊 Reliability experiments and visualizations
- 📥 Experiment results export to CSV

## 🛠️ Technologies

- Python
- Streamlit
- pandas
- reedsolo
- hashlib

## ⚙️ How It Works

1. Upload a file or enter text.
2. Convert the data into bytes and binary.
3. Map every two binary bits to a DNA base:
   - 00 → A
   - 01 → C
   - 10 → G
   - 11 → T
4. Simulate DNA mutations.
5. Attempt error correction with Reed–Solomon.
6. Decode the DNA sequence back into bytes.
7. Compare SHA-256 hashes to verify exact recovery.

## 🚀 Run Locally

Clone the repository:

    git clone YOUR_GITHUB_REPOSITORY_URL

Open the project folder:

    cd DNA-Storage-Lab

Install dependencies:

    python -m pip install -r requirements.txt

Start the application:

    python -m streamlit run app.py

## ⚠️ Limitations

This is an educational software simulation. It does not synthesize,
sequence, or physically store DNA.

The encoding scheme uses a simple two-bit mapping and does not
implement biological sequence constraints.

Results from mutation experiments may vary because mutations are
randomly generated.

## 🎓 Project

B.Tech Computer Science Engineering — Artificial Intelligence
and Machine Learning

## 📄 License

MIT License