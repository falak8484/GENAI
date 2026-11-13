# OWASPShield – Prompt Comparison and Evaluation

## 1. Objective

The purpose of this evaluation is to compare two prompt versions (V1 and V2) used by OWASPShield.

The comparison focuses on response quality, accuracy, relevance, clarity, completeness, and handling of dataset limitations.

Both versions are tested using the same 10 cybersecurity questions.

## 2. Evaluation Questions

1. How should I store user passwords securely?
2. Which password hashing algorithm should I use?
3. Why should every password have a unique salt?
4. How can I protect login endpoints against repeated failed attempts?
5. How can I prevent SQL injection when accepting user input?
6. How can I configure AWS CloudTrail to detect suspicious API activity?
7. Why is multifactor authentication important?
8. What authentication protections should a login system include?
9. What are the risks of storing passwords using weak hashing methods?
10. Which OWASP Top 10 categories are covered by the current OWASPShield records?

## 3. Evaluation Criteria

Each prompt version is evaluated using five criteria.

| Criteria | Description | Maximum Score |
|---|---|---:|
| Accuracy | Is the technical information correct? | 5 |
| Relevance | Does the answer address the question? | 5 |
| Clarity | Is the answer easy to understand? | 5 |
| Completeness | Does the answer cover important points? | 5 |
| Dataset Awareness | Does the answer handle dataset limitations appropriately? | 5 |
| **Total** | | **25** |

Scores are assigned manually by reviewing the generated responses.

**Important:** The current `/evaluate` endpoint sends the selected evaluation prompt and user question to the LLM. It does not retrieve or include actual OWASPShield records. Therefore, dataset-awareness scores are preliminary and do not prove that the model used the dataset.

## 4. Prompt Comparison Results

| Question | V1 Score | V2 Score | Observation |
|---|---:|---:|---|
| Q1 | 22/25 | 21/25 | V1 provided more detail, including optional pepper protection. V2 was more concise and readable. |
| Q2 | 22/25 | 23/25 | V1 provided detailed algorithm explanations. V2 was better structured and included practical secure-coding advice. |
| Q3 | 22/25 | 21/25 | V1 provided a more detailed and technically precise explanation. V2 was more concise but used a slightly misleading secret-ingredient analogy for salts. |
| Q4 | Pending | Pending | Not tested yet. |
| Q5 | Pending | Pending | Not tested yet. |
| Q6 | Pending | Pending | Not tested yet. |
| Q7 | Pending | Pending | Not tested yet. |
| Q8 | Pending | Pending | Not tested yet. |
| Q9 | Pending | Pending | Not tested yet. |
| Q10 | Pending | Pending | Not tested yet. |

## 5. Detailed Evaluation

### Q1: How should I store user passwords securely?

**V1 Response:**
- Explained password hashing and why plaintext password storage is unsafe.
- Recommended Argon2, bcrypt and PBKDF2.
- Explained unique salts, key stretching and optional pepper protection.
- Included a practical password-storage workflow.

**V2 Response:**
- Explained password hashing and recommended modern password-hashing algorithms.
- Covered unique salts and cost factors.
- Presented the information in a more concise and readable structure.

**Scores:**

| Criteria | V1 | V2 |
|---|---:|---:|
| Accuracy | 4 | 4 |
| Relevance | 5 | 5 |
| Clarity | 4 | 5 |
| Completeness | 5 | 4 |
| Dataset Awareness | 4 | 3 |
| **Total** | **22/25** | **21/25** |

**Observation:**

V1 provided more detailed information, including optional pepper protection. V2 was easier to read and more concise. V1 received a slightly higher preliminary score because it covered more details.

### Q2: Which password hashing algorithm should I use?

**V1 Response:**
- Recommended Argon2, bcrypt and scrypt.
- Explained how salts protect password hashes.
- Discussed work factors and key stretching.
- Explained why MD5, SHA-1 and SHA-2 general-purpose hashes should not be used directly for password storage.

**V2 Response:**
- Recommended Argon2, scrypt and bcrypt.
- Explained memory-hardness, salting and adaptivity.
- Included practical secure-coding recommendations.
- Suggested using trusted cryptographic libraries and storing the complete password-hash output.

**Scores:**

| Criteria | V1 | V2 |
|---|---:|---:|
| Accuracy | 5 | 5 |
| Relevance | 5 | 5 |
| Clarity | 4 | 5 |
| Completeness | 5 | 5 |
| Dataset Awareness | 3 | 3 |
| **Total** | **22/25** | **23/25** |

**Observation:**

V1 provided detailed explanations of the recommended algorithms. V2 presented the information more clearly and included additional practical secure-coding advice.

**Winner: V2**

V2 was slightly clearer and more practical while maintaining technical accuracy.

### Q3: Why should every password have a unique salt?

**V1 Response:**
- Explained password hashing and the purpose of salts.
- Described rainbow table attacks.
- Explained how unique salts produce different hashes for identical passwords.
- Discussed batch password cracking and brute-force attacks.
- Included a practical lockbox analogy.

**V2 Response:**
- Explained what a salt is and why it should be unique.
- Covered rainbow tables and pre-computation attacks.
- Explained why identical passwords should produce different hashes.
- Included secure coding practices for generating and storing salts.

**Scores:**

| Criteria | V1 | V2 |
|---|---:|---:|
| Accuracy | 5 | 4 |
| Relevance | 5 | 5 |
| Clarity | 4 | 4 |
| Completeness | 5 | 5 |
| Dataset Awareness | 3 | 3 |
| **Total** | **22/25** | **21/25** |

**Observation:**

V1 provided a more detailed explanation with a practical analogy. V2 was shorter and well structured, but its secret-ingredient analogy could incorrectly suggest that salts must remain secret. In reality, salts do not need to be secret and are stored alongside password hashes.

**Winner: V1**

V1 provided a slightly more technically precise explanation.

## 6. Final Comparison

This section will be completed after testing all 10 questions.

The final comparison will include:

- Total score for V1.
- Total score for V2.
- Average score for each version.
- Strengths and weaknesses of each prompt.
- Selection of the better-performing prompt version.

## 7. Dataset Limitation Test

Question Q6 is intentionally outside the current OWASPShield dataset.

**Question:** How can I configure AWS CloudTrail to detect suspicious API activity?

The current dataset contains:

- Authentication Cheat Sheet
- Password Storage Cheat Sheet
- SQL Injection Prevention Cheat Sheet

It does not contain AWS CloudTrail or cloud audit-log information.

**Expected behaviour:**

OWASPShield should clearly explain that the current dataset does not cover AWS CloudTrail rather than pretending that the information exists in its records.

**Note:** The current evaluation endpoint does not pass the actual dataset to the LLM. A proper dataset-awareness test requires integrating record retrieval into the evaluation workflow.

## 8. Conclusion

The evaluation is being conducted using two prompt versions and 10 cybersecurity questions.

The objective is to identify which prompt produces more accurate, relevant, clear, complete and appropriately cautious responses.

The final conclusion will be added after all 10 questions have been tested.