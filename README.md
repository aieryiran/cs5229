# cs5229

CS5229 Homework 4 Description

Student: Wen Yiran / A0105610Y
Date: 2020 Oct 27

------------------------------------------------------------------------------------

Policy 1:
H1-H3 TCP and H1-H4 UDP traffic are sharing the 100MB throughput limit betwee S1 S3 connection. 
When the usage is close to 100MB, the policy the redirect the H1-H4 UDP package to go another route of H1 - S1 - S2 - S3 - H4.

------------------------------------------------------------------------------------

Policy 2:
H1-H3 TCP, H1-H4 UDP and H1-H5 UDP traffic are sharing the 100MB throughput limit betwee S1 S3 connection. 
When the usage is close to 100MB, the policy the redirect the H1-H4 UDP and H1-H5 UDP package to go another route of H1 - S1 - S2 - S3 - H4 and H1 - S1 - S2 - S3 - H5.

------------------------------------------------------------------------------------

Policy 3:
H2-H3 TCP and H2-H5 UDP traffic are sharing the 100MB throughput limit betwee S2 S3 connection.
H1-H4 UDP traffic is using the 100MB throughput limit betwee S1 S3 connection.
When the S2-S3 usage is close to 100MB, the policy the redirect the H2-H5 UDP package to go another route of H2 - S2 - S1 - S3 - H5.