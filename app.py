import hashlib
import random
import streamlit as st
from reedsolo import RSCodec, ReedSolomonError

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="DNA Storage Lab 2.0",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧬 DNA Storage Lab 2.0")


st.markdown(
    """
    ### Multimedia Storage Using DNA Encoding

    Convert text, images, and videos into simulated DNA sequences.
    Explore data integrity, random mutations, and error correction.

    **Project modules:** Encoding • Decoding • Integrity • Reliability
    """
)
with st.sidebar:
    st.header("🧬 DNA Storage Lab")

    st.write("**Project Dashboard**")

    st.markdown("---")

    st.subheader("Available Features")

    st.write("📝 Text encoding")
    st.write("🖼️ Image encoding")
    st.write("🎥 Video encoding")
    st.write("🔐 SHA-256 integrity checking")
    st.write("🛡️ Reed–Solomon error correction")
    st.write("📊 Reliability experiments")

    st.markdown("---")

    st.caption(
        "Educational simulation only. "
        "No physical DNA synthesis is performed."
    )
st.divider()

st.write(
    "A multimedia DNA storage simulator for text, images, and videos."
)

st.info(
    "This is a software simulation. It encodes file bytes into "
    "A, C, G, and T; it does not synthesize real DNA."
)

# -----------------------------------
# DNA ENCODING
# -----------------------------------

DNA_MAP = {
    "00": "A",
    "01": "C",
    "10": "G",
    "11": "T"
}

REVERSE_MAP = {
    value: key for key, value in DNA_MAP.items()
}


def encode_bytes(data):
    """Convert bytes into a simulated DNA sequence."""

    binary = "".join(
        format(byte, "08b")
        for byte in data
    )

    dna = "".join(
        DNA_MAP[binary[i:i + 2]]
        for i in range(0, len(binary), 2)
    )

    return dna


def decode_dna(dna):
    """Convert DNA sequence back into bytes."""

    if any(base not in REVERSE_MAP for base in dna):
        raise ValueError("DNA contains an invalid base.")

    binary = "".join(
        REVERSE_MAP[base]
        for base in dna
    )

    if len(binary) % 8 != 0:
        raise ValueError("Invalid DNA sequence length.")

    return bytes(
        int(binary[i:i + 8], 2)
        for i in range(0, len(binary), 8)
    )


def calculate_hash(data):
    """Calculate SHA-256 to verify exact reconstruction."""

    return hashlib.sha256(data).hexdigest()



# -----------------------------------
# REED-SOLOMON ERROR CORRECTION
# -----------------------------------

def protect_data(data, parity_bytes=16):
    """Add Reed-Solomon redundancy to the original bytes."""
    codec = RSCodec(parity_bytes)
    return bytes(codec.encode(data))


def correct_data(protected_data, parity_bytes=16):
    """Attempt to correct errors in protected bytes."""
    codec = RSCodec(parity_bytes)
    corrected = codec.decode(protected_data)
    return bytes(corrected[0])


# -----------------------------------
# STORAGE MODE
# -----------------------------------

mode = st.radio(
    "Choose storage type",
    ["Text", "Image", "Video"],
    horizontal=True
)

original_bytes = None
filename = None
mime_type = None

# -----------------------------------
# TEXT STORAGE
# -----------------------------------

if mode == "Text":

    text_input = st.text_area(
        "Enter the text you want to store",
        value="Hello from DNA Storage Lab!"
    )

    original_bytes = text_input.encode("utf-8")
    filename = "recovered_text.txt"
    mime_type = "text/plain"

# -----------------------------------
# IMAGE STORAGE
# -----------------------------------

elif mode == "Image":

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_file is not None:

        original_bytes = uploaded_file.getvalue()
        filename = uploaded_file.name
        mime_type = uploaded_file.type

        st.image(
            original_bytes,
            caption="Original uploaded image",
            use_container_width=True
        )

# -----------------------------------
# VIDEO STORAGE
# -----------------------------------

elif mode == "Video":

    uploaded_file = st.file_uploader(
        "Upload a video",
        type=["mp4", "mov", "webm"]
    )

    if uploaded_file is not None:

        original_bytes = uploaded_file.getvalue()
        filename = uploaded_file.name
        mime_type = uploaded_file.type

        st.video(original_bytes)

# -----------------------------------
# ENCODE AND RECONSTRUCT
# -----------------------------------

if original_bytes is not None:

    st.divider()
    st.header("DNA Storage Results")

    dna_sequence = encode_bytes(original_bytes)

    # Reconstruct the original file bytes.
    recovered_bytes = decode_dna(dna_sequence)

    # Verify the original and reconstructed files.
    original_hash = calculate_hash(original_bytes)
    recovered_hash = calculate_hash(recovered_bytes)

    integrity_ok = original_hash == recovered_hash

    # Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Original size",
        f"{len(original_bytes):,} bytes"
    )

    col2.metric(
        "DNA bases",
        f"{len(dna_sequence):,}"
    )

    col3.metric(
        "Bases per byte",
        f"{len(dna_sequence) / len(original_bytes):.1f}"
        if original_bytes else "0"
    )

    # Display sequence
    with st.expander("View simulated DNA sequence"):

        st.code(
            dna_sequence[:5000]
            if dna_sequence
            else "(empty sequence)"
        )

        if len(dna_sequence) > 5000:
            st.caption(
                "Only the first 5,000 bases are displayed."
            )

    # Verify reconstruction
    if integrity_ok:
        st.success(
            "Integrity check passed: reconstructed bytes "
            "match the original file exactly."
        )
    else:
        st.error("Integrity check failed.")

    st.write("SHA-256 of original file:")
    st.code(original_hash)

    st.write("SHA-256 of reconstructed file:")
    st.code(recovered_hash)

    # Download reconstructed file
    st.download_button(
        label="Download reconstructed file",
        data=recovered_bytes,
        file_name=filename,
        mime=mime_type or "application/octet-stream"
    )

    # Download DNA sequence
    st.download_button(
        label="Download DNA sequence",
        data=dna_sequence,
        file_name="simulated_dna_sequence.txt",
        mime="text/plain"
    )

    st.caption(
        "This demo encodes each byte into four DNA bases. "
        "The DNA sequence is a simulated representation, not "
        "a physical storage medium."
    )




# # -----------------------------------
# # MULTIMEDIA DNA DAMAGE LAB
# # -----------------------------------

# st.divider()
# st.header("🧪 Multimedia DNA Reliability Lab")

# st.write(
#     "Simulate substitutions in a DNA sequence and test "
#     "whether the original file can still be reconstructed."
# )

# error_rate = st.slider(
#     "DNA substitution error rate (%)",
#     min_value=0,
#     max_value=20,
#     value=5,
#     step=1,
#     key="multimedia_error_rate"
# )

# if st.button("Run DNA damage experiment"):

#     import random

#     rng = random.Random(42)

#     dna_bases = ["A", "C", "G", "T"]
#     damaged_dna = list(dna_sequence)

#     changed_bases = 0

#     for i in range(len(damaged_dna)):

#         if rng.random() < error_rate / 100:

#             alternatives = [
#                 base for base in dna_bases
#                 if base != damaged_dna[i]
#             ]

#             damaged_dna[i] = rng.choice(alternatives)
#             changed_bases += 1

#     damaged_dna = "".join(damaged_dna)

#     st.subheader("Experiment Results")

#     col1, col2, col3 = st.columns(3)

#     col1.metric(
#         "Original DNA bases",
#         f"{len(dna_sequence):,}"
#     )

#     col2.metric(
#         "Changed bases",
#         f"{changed_bases:,}"
#     )

#     col3.metric(
#         "Actual error rate",
#         f"{changed_bases / len(dna_sequence) * 100:.2f}%"
#         if dna_sequence else "0.00%"
#     )

#     try:

#         recovered_after_damage = decode_dna(damaged_dna)

#         recovery_success = (
#             recovered_after_damage == original_bytes
#         )

#     except (ValueError, UnicodeDecodeError):

#         recovered_after_damage = None
#         recovery_success = False

#     if recovery_success:

#         st.success(
#             "The reconstructed file matches the original bytes."
#         )

#     else:

#         st.error(
#             "The reconstructed data differs from the original "
#             "or could not be decoded."
#         )

#     if recovered_after_damage is not None:

#         st.write("Original SHA-256")
#         st.code(calculate_hash(original_bytes))

#         st.write("Recovered SHA-256")
#         st.code(calculate_hash(recovered_after_damage))

#         st.download_button(
#             "Download damaged reconstruction",
#             data=recovered_after_damage,
#             file_name=f"damaged_{filename}",
#             mime="application/octet-stream"
#         )

#     with st.expander("View damaged DNA sequence"):

#         st.code(
#             damaged_dna[:5000]
#             if damaged_dna
#             else "(empty sequence)"
#         )

#         if len(damaged_dna) > 5000:

#             st.caption(
#                 "Only the first 5,000 bases are displayed."
#             )

#     st.caption(
#         "This experiment models substitution errors only. "
#         "It does not model insertions, deletions, or physical "
#         "DNA synthesis and sequencing."
#     )



# -----------------------------------
# MULTIMEDIA ERROR CORRECTION LAB
# -----------------------------------

st.divider()
st.header("🛡️ Multimedia Error Correction Lab")

st.write(
    "Compare ordinary DNA encoding with Reed-Solomon "
    "error correction."
)

parity_bytes = st.select_slider(
    "Redundancy level (parity bytes)",
    options=[8, 16, 32, 64],
    value=16,
    key="rs_parity"
)

rs_error_rate = st.slider(
    "Substitution error rate (%)",
    min_value=0,
    max_value=20,
    value=5,
    step=1,
    key="rs_error_rate"
)

if st.button("Run error-correction experiment"):

    # Protect the original file bytes.
    protected_bytes = protect_data(
        original_bytes,
        parity_bytes
    )

    # Encode protected bytes into simulated DNA.
    protected_dna = encode_bytes(protected_bytes)

    # Introduce substitutions into the DNA sequence.
    rng = random.Random(42)
    bases = ["A", "C", "G", "T"]
    damaged_dna = list(protected_dna)

    changed_bases = 0

    for i in range(len(damaged_dna)):

        if rng.random() < rs_error_rate / 100:

            alternatives = [
                base for base in bases
                if base != damaged_dna[i]
            ]

            damaged_dna[i] = rng.choice(alternatives)
            changed_bases += 1

    damaged_dna = "".join(damaged_dna)

    st.write(f"DNA substitutions introduced: {changed_bases:,}")

    # Decode DNA bases back into protected bytes.
    damaged_protected_bytes = decode_dna(damaged_dna)

    try:

        recovered_bytes = correct_data(
            damaged_protected_bytes,
            parity_bytes
        )

        success = recovered_bytes == original_bytes

    except (ReedSolomonError, ValueError, IndexError):

        recovered_bytes = None
        success = False

    if success:

        st.success(
            "Success! Error correction recovered the original file."
        )

        st.write("Original SHA-256")
        st.code(calculate_hash(original_bytes))

        st.write("Recovered SHA-256")
        st.code(calculate_hash(recovered_bytes))

        st.download_button(
            "Download corrected file",
            data=recovered_bytes,
            file_name=f"corrected_{filename}",
            mime=mime_type or "application/octet-stream"
        )

    else:

        st.error(
            "Exact recovery failed. The corruption may exceed "
            "the correction capability of the selected code."
        )

    st.metric(
        "Encoded DNA length",
        f"{len(protected_dna):,} bases"
    )

    st.metric(
        "Redundancy overhead",
        f"{(len(protected_bytes) / len(original_bytes) - 1) * 100:.1f}%"
        if original_bytes else "0%"
    )

    st.caption(
        "Results are from a simulated substitution-error model, "
        "not a physical DNA storage experiment."
    )




# -----------------------------------
# STORAGE ANALYSIS
# -----------------------------------

st.divider()
st.header("📊 DNA Storage Analysis")

st.write(
    "Compare the original file size with the theoretical "
    "size of its simulated DNA representation."
)

if original_bytes is not None:

    original_size = len(original_bytes)
    dna_bases = len(encode_bytes(original_bytes))

    # Each DNA base represents two bits in this encoding.
    theoretical_dna_bytes = (dna_bases * 2 + 7) // 8

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Original file",
        f"{original_size:,} bytes"
    )

    col2.metric(
        "DNA bases",
        f"{dna_bases:,}"
    )

    col3.metric(
        "Encoded information size",
        f"{theoretical_dna_bytes:,} bytes"
    )

    st.caption(
        "The encoded information size is a theoretical bit-count "
        "comparison, not the physical size of DNA molecules. "
        "It excludes synthesis, sequencing, indexing, and other costs."
    )




st.divider()
st.header("🧪 Automated DNA Reliability Experiment")

if original_bytes is not None:
    st.write("Test how random DNA mutations affect your stored file.")

    error_rates = [0, 1, 2, 5, 10]

    results = []

    original_dna = encode_bytes(original_bytes)

    for rate in error_rates:
        damaged_dna = list(original_dna)

        number_of_errors = int(len(damaged_dna) * rate / 100)

        if number_of_errors > 0:
            positions = random.sample(
                range(len(damaged_dna)),
                min(number_of_errors, len(damaged_dna))
            )

            for position in positions:
                current_base = damaged_dna[position]
                possible_bases = [
                    base for base in ["A", "C", "G", "T"]
                    if base != current_base
                ]
                damaged_dna[position] = random.choice(possible_bases)

        damaged_dna = "".join(damaged_dna)

        try:
            recovered_bytes = decode_dna(damaged_dna)

            matching = recovered_bytes == original_bytes

            results.append({
                "Mutation Rate (%)": rate,
                "Mutated Bases": number_of_errors,
                "Exact Recovery": "Yes" if matching else "No"
            })

        except Exception:
            results.append({
                "Mutation Rate (%)": rate,
                "Mutated Bases": number_of_errors,
                "Exact Recovery": "No"
            })

    import pandas as pd

    results_df = pd.DataFrame(results)

    st.dataframe(results_df, use_container_width=True)

    st.caption(
        "This experiment simulates random base substitutions. "
        "Results may vary because mutations are randomly selected."
    )




st.subheader("📈 Mutation Rate vs Data Recovery")

# Convert recovery results into numerical values
results_df["Recovery Score (%)"] = results_df["Exact Recovery"].map({
    "Yes": 100,
    "No": 0
})

# Display line chart
st.line_chart(
    results_df.set_index("Mutation Rate (%)")["Recovery Score (%)"]
)

# Display bar chart
st.subheader("📊 Recovery Score at Each Mutation Rate")

st.bar_chart(
    results_df.set_index("Mutation Rate (%)")["Recovery Score (%)"]
)



csv_data = results_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Experiment Results (CSV)",
    data=csv_data,
    file_name="dna_reliability_results.csv",
    mime="text/csv"
)   



st.divider()
st.header("🛡️ DNA Recovery: Before vs After Error Correction")

if original_bytes is not None:
    st.write(
        "Compare exact file recovery with and without "
        "Reed–Solomon error correction."
    )

    parity_bytes = st.selectbox(
        "Select error-correction strength (parity bytes)",
        [8, 16, 32, 64],
        index=1,
        key="comparison_parity"
    )

    mutation_rate = st.slider(
        "Select DNA mutation rate (%)",
        min_value=0,
        max_value=10,
        value=2,
        key="comparison_mutation"
    )

    if st.button("Run Recovery Comparison"):
        try:
            # Protect the original data
            protected_data = protect_data(
                original_bytes,
                parity_bytes
            )

            # Convert protected bytes into DNA
            protected_dna = encode_bytes(protected_data)

            # Introduce random base substitutions
            damaged_dna = list(protected_dna)

            error_count = int(
                len(damaged_dna) * mutation_rate / 100
            )

            if error_count > 0:
                positions = random.sample(
                    range(len(damaged_dna)),
                    min(error_count, len(damaged_dna))
                )

                for position in positions:
                    old_base = damaged_dna[position]

                    choices = [
                        base for base in "ACGT"
                        if base != old_base
                    ]

                    damaged_dna[position] = random.choice(choices)

            damaged_dna = "".join(damaged_dna)

            # Decode the damaged DNA
            damaged_bytes = decode_dna(damaged_dna)

            # Check recovery without correction
            # Compare against the original file
            without_correction = (
                damaged_bytes[:len(original_bytes)]
                == original_bytes
                and len(damaged_bytes) == len(original_bytes)
            )

            # Try Reed-Solomon correction
            corrected_bytes = correct_data(
                damaged_bytes,
                parity_bytes
            )

            with_correction = corrected_bytes == original_bytes

            # Display results
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Without Error Correction",
                    "Success" if without_correction else "Failed"
                )

            with col2:
                st.metric(
                    "With Reed–Solomon",
                    "Success" if with_correction else "Failed"
                )

            comparison_df = pd.DataFrame({
                "Method": [
                    "Without Error Correction",
                    "With Reed–Solomon"
                ],
                "Exact Recovery (%)": [
                    100 if without_correction else 0,
                    100 if with_correction else 0
                ]
            })

            st.bar_chart(
                comparison_df.set_index("Method")
            )

            if with_correction:
                st.success(
                    "The original file was recovered successfully "
                    "after error correction!"
                )
            else:
                st.warning(
                    "Exact recovery failed. The mutation level may "
                    "exceed the correction capacity. Try a lower "
                    "mutation rate or a different parity setting."
                )

        except ReedSolomonError:
            st.error(
                "Reed–Solomon could not correct these errors. "
                "Try a lower mutation rate or more parity bytes."
            )

        except Exception as error:
            st.error(f"Experiment failed: {error}")



st.divider()
st.header("⚖️ DNA Storage vs Traditional Digital Storage")

comparison_data = {
    "Feature": [
        "Data representation",
        "Basic storage unit",
        "Encoding method in this project",
        "Human-readable directly",
        "Error detection",
        "Error correction",
        "Physical storage medium"
    ],
    "Traditional Digital Storage": [
        "Binary (0 and 1)",
        "Bits",
        "Binary representation",
        "No, for most file formats",
        "SHA-256 integrity check",
        "Depends on the storage system",
        "SSD, HDD, flash memory, etc."
    ],
    "DNA Storage": [
        "DNA bases (A, C, G, T)",
        "DNA bases",
        "2 bits mapped to each base",
        "No",
        "SHA-256 after decoding",
        "Reed–Solomon in this project",
        "Synthetic DNA molecules in real systems"
    ]
}

comparison_df = pd.DataFrame(comparison_data)

st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)

st.subheader("📦 Storage Size Comparison")

if original_bytes is not None:
    original_size = len(original_bytes)
    dna_sequence = encode_bytes(original_bytes)
    dna_bases = len(dna_sequence)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Original File",
        f"{original_size:,} bytes"
    )

    col2.metric(
        "DNA Sequence",
        f"{dna_bases:,} bases"
    )

    col3.metric(
        "Bases per Byte",
        f"{dna_bases / original_size:.1f}"
        if original_size > 0 else "N/A"
    )

st.info(
    "Educational simulation: this project maps every 2 bits to one "
    "DNA base. It does not synthesize or physically store DNA. "
    "Actual DNA storage also involves synthesis, sequencing, and "
    "additional overhead."
)