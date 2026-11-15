# OWASPShield Semantic Search Results

## Question 1: How should passwords be stored securely?

**Hit 1:** Store Passwords in a Secure Fashion
- Source: authentication.md
- Page: N/A
- Similarity score: 0.7712

- Retrieved text: Store Passwords in a Secure Fashion
It is critical for an application to store a password using the right cryptographic technique. Please see [Password Storage Cheat Sheet](Password_Storage_Cheat_Sheet.md) for details on this feature.

**Hit 2:** Introduction
- Source: password_storage.md
- Page: N/A
- Similarity score: 0.7698

- Retrieved text: Introduction
This cheat sheet advises you on the proper methods for storing passwords for authentication. When passwords are stored, they must be protected from an attacker even if the application or database is compromised. Fortunately, a majority of modern languages and frameworks provide built-in functionality to help store passwords safely.

Passwords should never be stored in plain text. Instead, they must be protected using strong, slow hashing algorithms such as Argon2id, bcrypt, or PBKDF2. A unique salt must be added to each password to prevent attackers from using precomputed lookup tables like rainbow tables. Fast hashing algorithms such as SHA‑256 are not suitable for password storage because they allow attackers to perform large numbers of guesses quickly. Using slow, memory‑hard algorithms makes brute‑force attacks significantly more difficult, expensive, and time‑consuming.

To sum up our recommendations:

**Hit 3:** Password Hashing Algorithms
- Source: password_storage.md
- Page: N/A
- Similarity score: 0.7508

- Retrieved text: Password Hashing Algorithms
Some modern hashing algorithms have been specifically designed to securely store passwords. This means that they should be slow (unlike algorithms such as MD5 and SHA-1, which were designed to be fast), and you can change how slow they are by changing the work factor.

You do not need to hide which password hashing algorithm is used by an application. If you utilize a modern password hashing algorithm with proper configuration parameters, it should be safe to state in public which password hashing algorithms are in use and be listed [here](https://pulse.michalspacek.cz/passwords/storages).

When selecting a password hashing algorithm, developers should prefer modern algorithms that are designed to resist both GPU-based and memory-based attacks.
Where available, newer algorithms should be chosen for new applications, while older algorithms may still be acceptable for legacy systems with appropriate configuration.

Three hashing algorithms that should be considered.

---

## Question 2: Why should each password have a unique salt?

**Hit 1:** Salting
- Source: password_storage.md
- Page: N/A
- Similarity score: 0.7776

- Retrieved text: Salting
A salt is a unique, randomly generated string that is added to each password as part of the hashing process. As the salt is unique for every user, an attacker has to crack hashes one at a time using the respective salt rather than calculating a hash once and comparing it against every stored hash. This makes cracking large numbers of hashes significantly harder, as the time required grows in direct proportion to the number of hashes.

Salting also protects against an attacker's pre-computing hashes using rainbow tables or database-based lookups. Finally, salting means that it is impossible to determine whether two users have the same password without cracking the hashes, as the different salts will result in different hashes even if the passwords are the same.

At the algorithm and specification level, modern password hashing functions such as [Argon2id](#argon2id), [bcrypt](#bcrypt), and [PBKDF2](#pbkdf2) require the caller to provide a salt.

**Hit 2:** Peppering
- Source: password_storage.md
- Page: N/A
- Similarity score: 0.7036

- Retrieved text: Peppering
[Peppering](https://datatracker.ietf.org/doc/html/draft-ietf-kitten-password-storage-07#section-4.2) is a class of strategies that can be used in addition to salting to provide an additional layer of protection. It prevents an attacker from being able to crack any of the hashes if they only have access to the database, for example, if they have exploited a SQL injection vulnerability or obtained a backup of the database.

**Hit 3:** Common requirements for peppering strategies
- Source: password_storage.md
- Page: N/A
- Similarity score: 0.6929

- Retrieved text: Common requirements for peppering strategies
- A pepper is **shared between stored passwords**, rather than being *unique* to an individual password like a password salt.
- Unlike a password salt, the pepper should not be public and **should not be stored along with the generated hash**. The pepper should be stored separately from the password database.
- Peppers are secrets and should be stored in "secrets vaults" or HSMs (Hardware Security Modules). See the [Secrets Management Cheat Sheet](Secrets_Management_Cheat_Sheet.md) for more information on securely storing secrets.
- In the event of a pepper's compromise, the pepper will have to be changed. Peppers cannot be changed without knowledge of a user's password. Therefore changing a pepper will require forcing all users whose passwords were protected by the previous pepper to reset their passwords.

---

## Question 3: What is the purpose of a password pepper?

**Hit 1:** Common requirements for peppering strategies
- Source: password_storage.md
- Page: N/A
- Similarity score: 0.7910

- Retrieved text: Common requirements for peppering strategies
- A pepper is **shared between stored passwords**, rather than being *unique* to an individual password like a password salt.
- Unlike a password salt, the pepper should not be public and **should not be stored along with the generated hash**. The pepper should be stored separately from the password database.
- Peppers are secrets and should be stored in "secrets vaults" or HSMs (Hardware Security Modules). See the [Secrets Management Cheat Sheet](Secrets_Management_Cheat_Sheet.md) for more information on securely storing secrets.
- In the event of a pepper's compromise, the pepper will have to be changed. Peppers cannot be changed without knowledge of a user's password. Therefore changing a pepper will require forcing all users whose passwords were protected by the previous pepper to reset their passwords.

**Hit 2:** Pre-hashing peppers
- Source: password_storage.md
- Page: N/A
- Similarity score: 0.7834

- Retrieved text: Pre-hashing peppers
In this strategy, a pepper is added to a password before being hashed by a password hashing algorithm. The computed hash is then stored in the database. In this case the pepper should be a random value generated securely. See the [Cryptographic_Storage_Cheat_Sheet](Cryptographic_Storage_Cheat_Sheet.md#secure-random-number-generation) for more information on securely generating random values.

**Hit 3:** Post-hashing peppers
- Source: password_storage.md
- Page: N/A
- Similarity score: 0.7779

- Retrieved text: Post-hashing peppers
In this strategy, a password is hashed as usual using a password hashing algorithm. The resulting password hash is then hashed again using an HMAC (e.g., HMAC-SHA256, HMAC-SHA512, depending on the desired output length) before storing the resulting hash in the database. In this case the pepper is acting as the HMAC key and should be generated as per requirements of the HMAC algorithm.

---

## Question 4: How does Argon2id protect stored passwords?

**Hit 1:** Argon2id
- Source: password_storage.md
- Page: N/A
- Similarity score: 0.7647

- Retrieved text: Argon2id
[Argon2](https://en.wikipedia.org/wiki/Argon2) was the winner of the 2015 [Password Hashing Competition](https://en.wikipedia.org/wiki/Password_Hashing_Competition). Out of the three Argon2 versions, use the  Argon2id variant since it provides a balanced approach to resisting both side-channel and GPU-based attacks.

Argon2id has three main cost parameters: total memory in KiB (m), the number of passes (t), and the degree of parallelism (p). Parallelism controls the number of lanes over which the memory is divided; increasing p does not multiply the total memory or act as an iteration count. See [RFC 9106 Section 3.1](https://www.rfc-editor.org/rfc/rfc9106.html#section-3.1) for the parameter definitions.

**Hit 2:** Argon2id
- Source: password_storage.md
- Page: N/A
- Similarity score: 0.7383

- Retrieved text: Argon2id
mory or act as an iteration count. See [RFC 9106 Section 3.1](https://www.rfc-editor.org/rfc/rfc9106.html#section-3.1) for the parameter definitions.

Tune memory and iteration costs to make password cracking expensive while keeping authentication practical under expected load. [Benchmark the chosen parameters on the target system](https://www.rfc-editor.org/rfc/rfc9106.html#section-4); increasing parallelism is not a guarantee of slower password guessing. Use one of the following minimum configurations:

- m=47104 (46 MiB), t=1, p=1 (Do not use with Argon2i)
- m=19456 (19 MiB), t=2, p=1 (Do not use with Argon2i)
- m=12288 (12 MiB), t=3, p=1
- m=9216 (9 MiB), t=4, p=1
- m=7168 (7 MiB), t=5, p=1

These configuration settings provide an equal level of defense, and the only difference is a trade off between CPU and RAM usage.

**Hit 3:** Introduction
- Source: password_storage.md
- Page: N/A
- Similarity score: 0.7276

- Retrieved text: Introduction
g slow, memory‑hard algorithms makes brute‑force attacks significantly more difficult, expensive, and time‑consuming.

To sum up our recommendations:

- **Use [Argon2id](#argon2id) with a minimum configuration of 19 MiB of memory, an iteration count of 2, and 1 degree of parallelism.**
- **If [Argon2id](#argon2id) is not available, use [scrypt](#scrypt) with a minimum CPU/memory cost parameter of (2^17), a minimum block size of 8 (1024 bytes), and a parallelization parameter of 1.**
- **For legacy systems using [bcrypt](#bcrypt), use a work factor of 10 or more and with a password limit of 72 bytes.**
- **If FIPS-140 compliance is required, use [PBKDF2](#pbkdf2) with a work factor of 600,000 or more and set with an internal hash function of HMAC-SHA-256.**
- **Consider using a [pepper](#peppering) to provide additional defense in depth (though alone, it provides no additional secure characteristics).**

---

## Question 5: How can applications prevent brute-force login attacks?

**Hit 1:** Account Lockout
- Source: authentication.md
- Page: N/A
- Similarity score: 0.8012

- Retrieved text: Account Lockout
The most common protection against these attacks is to implement account lockout, which prevents any more login attempts for a period after a certain number of failed logins.

The counter of failed logins should be associated with the account itself, rather than the source IP address, in order to prevent an attacker from making login attempts from a large number of different IP addresses. There are a number of different factors that should be considered when implementing an account lockout policy in order to find a balance between security and usability:

- The number of failed attempts before the account is locked out (lockout threshold).
- The time period that these attempts must occur within (observation window).
- How long the account is locked out for (lockout duration).

**Hit 2:** CAPTCHA
- Source: authentication.md
- Page: N/A
- Similarity score: 0.7761

- Retrieved text: CAPTCHA
The use of an effective CAPTCHA can help to prevent automated login attempts against accounts. However, many CAPTCHA implementations have weaknesses that allow them to be solved using automated techniques or can be outsourced to services that can solve them. As such, the use of CAPTCHA should be viewed as a defense-in-depth control to make brute-force attacks more time-consuming and expensive, rather than as a preventative.

It may be more user-friendly to only require a CAPTCHA be solved after a small number of failed login attempts, rather than requiring it from the very first login.

**Hit 3:** Multi-Factor Authentication
- Source: authentication.md
- Page: N/A
- Similarity score: 0.7749

- Retrieved text: Multi-Factor Authentication
Multi-factor authentication (MFA) is by far the best defense against the majority of password-related attacks, including brute-force attacks, with analysis by Microsoft suggesting that it would have stopped [99.9% of account compromises](https://techcommunity.microsoft.com/t5/Azure-Active-Directory-Identity/Your-Pa-word-doesn-t-matter/ba-p/731984). As such, it should be implemented wherever possible; however, depending on the audience of the application, it may not be practical or feasible to enforce the use of MFA.

The [Multifactor Authentication Cheat Sheet](Multifactor_Authentication_Cheat_Sheet.md) contains further guidance on implementing MFA.

---

## Question 6: Why is multifactor authentication important?

**Hit 1:** Multi-Factor Authentication
- Source: authentication.md
- Page: N/A
- Similarity score: 0.6992

- Retrieved text: Multi-Factor Authentication
Multi-factor authentication (MFA) is by far the best defense against the majority of password-related attacks, including brute-force attacks, with analysis by Microsoft suggesting that it would have stopped [99.9% of account compromises](https://techcommunity.microsoft.com/t5/Azure-Active-Directory-Identity/Your-Pa-word-doesn-t-matter/ba-p/731984). As such, it should be implemented wherever possible; however, depending on the audience of the application, it may not be practical or feasible to enforce the use of MFA.

The [Multifactor Authentication Cheat Sheet](Multifactor_Authentication_Cheat_Sheet.md) contains further guidance on implementing MFA.

**Hit 2:** Adaptive or Risk Based Authentication
- Source: authentication.md
- Page: N/A
- Similarity score: 0.6919

- Retrieved text: Adaptive or Risk Based Authentication
A feature of more advanced applications is the ability to require different authentication stages depending on various environmental and contextual attributes (including but not limited to, the sensitivity of the data for which access is being requested, time of day, user location, IP address, or device fingerprint).

For example, an application may require MFA for the first login from a particular device but not for subsequent logins from that device. Alternatively, a single sign-on solution may authenticate the user and allow them to remain logged in for a day but require a reauthentication if they try to access their profile page.

**Hit 3:** Use of authentication protocols that require no password
- Source: authentication.md
- Page: N/A
- Similarity score: 0.6782

- Retrieved text: Use of authentication protocols that require no password
While authentication through a combination of username, password, and multi-factor authentication is considered generally secure, there are use cases where it isn't considered the best option or even safe. Examples of this are third-party applications that desire to connect to the web application, either from a mobile device, another website, desktop, or other situations. When this happens, it is NOT considered safe to allow the third-party application to store the user/password combo, since then it extends the attack surface into their hands, where it isn't in your control. For this and other use cases, there are several authentication protocols that can protect you from exposing your users' data to attackers.

---

## Question 7: How do parameterized queries prevent SQL injection?

**Hit 1:** Parameterized Queries
- Source: sql_injection.md
- Page: N/A
- Similarity score: 0.7629

- Retrieved text: Parameterized Queries
Define the SQL structure separately from its data values and bind those values through the database API, as shown in the [Basic SQL injection](#basic-sql-injection) example. Concatenating untrusted values into the query before preparing it defeats this protection.

See the [Query Parameterization Cheat Sheet](Query_Parameterization_Cheat_Sheet.md) for additional examples of parameterized queries in several languages, including Java, .NET, Ruby, PHP, Cold Fusion, Perl, and Rust. Other examples can be found at [Bobby Tables](https://bobby-tables.com/).

**Hit 2:** Primary Defenses
- Source: sql_injection.md
- Page: N/A
- Similarity score: 0.7389

- Retrieved text: Primary Defenses
The preferred patterns are:

- **parameterized queries** when including dynamic data in SQL requests;
- for structural parts that cannot be parameterized (table names, column names, sort direction), map user choices to a **strict allow-list** of fixed, application-owned values.

Relying on manually escaping dynamic inputs is error-prone and is strongly discouraged.

**Hit 3:** References
- Source: sql_injection.md
- Page: N/A
- Similarity score: 0.7362

- Retrieved text: References
- [Oracle JDBC: Using Prepared Statements](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)
- [PostgreSQL: Executing Dynamic Commands](https://www.postgresql.org/docs/current/plpgsql-statements.html#PLPGSQL-STATEMENTS-EXECUTING-DYN)
- [PHP PDO: Parameter-Marker Limitations](https://www.php.net/manual/en/pdo.prepare.php)

---

## Question 8: What should developers do when table names must be selected dynamically?

**Hit 1:** Allow-List Input Validation
- Source: sql_injection.md
- Page: N/A
- Similarity score: 0.7464

- Retrieved text: Allow-List Input Validation
Parameter markers represent data values, not table names, column names, or SQL keywords such as `ASC` and `DESC`; see the [PDO parameter-marker limitations](https://www.php.net/manual/en/pdo.prepare.php). Keep these structural choices fixed in code where possible. When users need to select among them, map their selection to a small set of application-owned values allowed for that query and reject anything else. In this example, `tableName` can only hold one of two fixed values, so it can be appended to the query:

```java
String tableName;
switch(PARAM) {
  case "room":
    tableName = "roomTable";
    break;
  case "floor":
    tableName = "floorTable";
    break;
  default:
    throw new InputValidationException("unexpected table name");
}
```

Map a requested sort direction the same way, to the literal `ASC` or `DESC`, rather than appending the supplied text.

**Hit 2:** References
- Source: sql_injection.md
- Page: N/A
- Similarity score: 0.7349

- Retrieved text: References
- [Oracle JDBC: Using Prepared Statements](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)
- [PostgreSQL: Executing Dynamic Commands](https://www.postgresql.org/docs/current/plpgsql-statements.html#PLPGSQL-STATEMENTS-EXECUTING-DYN)
- [PHP PDO: Parameter-Marker Limitations](https://www.php.net/manual/en/pdo.prepare.php)

**Hit 3:** Primary Defenses
- Source: sql_injection.md
- Page: N/A
- Similarity score: 0.7281

- Retrieved text: Primary Defenses
The preferred patterns are:

- **parameterized queries** when including dynamic data in SQL requests;
- for structural parts that cannot be parameterized (table names, column names, sort direction), map user choices to a **strict allow-list** of fixed, application-owned values.

Relying on manually escaping dynamic inputs is error-prone and is strongly discouraged.

---

## Question 9: Why should database accounts follow least privilege?

**Hit 1:** Details Of Least Privilege When Developing
- Source: sql_injection.md
- Page: N/A
- Similarity score: 0.7574

- Retrieved text: Details Of Least Privilege When Developing
If an account only needs access to portions of a table, consider creating a view that limits access to that portion of the data and assigning the account access to the view instead of the underlying table. Rarely, if ever, grant create or delete access to database accounts.

If you adopt a policy where you use stored procedures everywhere, and don't allow application accounts to directly execute their own queries, then restrict those accounts to only be able to execute the stored procedures they need. Don't grant them any rights directly to the tables in the database.

**Hit 2:** Enhancing Least Privilege with SQL Views
- Source: sql_injection.md
- Page: N/A
- Similarity score: 0.7531

- Retrieved text: Enhancing Least Privilege with SQL Views
You can use SQL views to further increase the granularity of access by limiting the read access to specific fields of a table or joins of tables. It could have additional benefits.

For example, a product catalog can use a view that exposes product names and retail prices while omitting supplier costs. Grant the application's database account only `SELECT` access to that view, without access to the underlying table or other objects that expose the omitted fields. Verify your database's view privilege rules; for example, [PostgreSQL normally checks underlying table access using the view owner's privileges](https://www.postgresql.org/docs/current/sql-createview.html).

This limits the data exposed through a compromised application account. Queries against views still require parameterization to prevent SQL injection.

**Hit 3:** Least Privilege
- Source: sql_injection.md
- Page: N/A
- Similarity score: 0.7380

- Retrieved text: Least Privilege
To minimize the potential damage of a successful SQL injection attack, you should minimize the privileges assigned to every database account in your environment. Start from the ground up to determine what access rights your application accounts require, rather than trying to figure out what access rights you need to take away.

Make sure that accounts that only need read access are only granted read access to the tables they need access to. DO NOT ASSIGN DBA OR ADMIN TYPE ACCESS TO YOUR APPLICATION ACCOUNTS. We understand that this is easy, and everything just "works" when you do it this way, but it is very dangerous.

---

## Question 10: How can applications protect passwords during transmission?

**Hit 1:** Transmit Passwords Only Over TLS or Other Strong Transport
- Source: authentication.md
- Page: N/A
- Similarity score: 0.7661

- Retrieved text: Transmit Passwords Only Over TLS or Other Strong Transport
See: [Transport Layer Security Cheat Sheet](Transport_Layer_Security_Cheat_Sheet.md)

The login page and all subsequent authenticated pages must be exclusively accessed over TLS or other strong transport. Failure to utilize TLS or other strong transport for the login page allows an attacker to modify the login form action, causing the user's credentials to be posted to an arbitrary location. Failure to utilize TLS or other strong transport for authenticated pages after login enables an attacker to view the unencrypted session ID and compromise the user's authenticated session.

**Hit 2:** Store Passwords in a Secure Fashion
- Source: authentication.md
- Page: N/A
- Similarity score: 0.7440

- Retrieved text: Store Passwords in a Secure Fashion
It is critical for an application to store a password using the right cryptographic technique. Please see [Password Storage Cheat Sheet](Password_Storage_Cheat_Sheet.md) for details on this feature.

**Hit 3:** Password Hashing Algorithms
- Source: password_storage.md
- Page: N/A
- Similarity score: 0.7165

- Retrieved text: Password Hashing Algorithms
Some modern hashing algorithms have been specifically designed to securely store passwords. This means that they should be slow (unlike algorithms such as MD5 and SHA-1, which were designed to be fast), and you can change how slow they are by changing the work factor.

You do not need to hide which password hashing algorithm is used by an application. If you utilize a modern password hashing algorithm with proper configuration parameters, it should be safe to state in public which password hashing algorithms are in use and be listed [here](https://pulse.michalspacek.cz/passwords/storages).

When selecting a password hashing algorithm, developers should prefer modern algorithms that are designed to resist both GPU-based and memory-based attacks.
Where available, newer algorithms should be chosen for new applications, while older algorithms may still be acceptable for legacy systems with appropriate configuration.

Three hashing algorithms that should be considered.

---
