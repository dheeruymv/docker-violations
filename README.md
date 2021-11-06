# Docker-violations

This tool finds the violations in the docker file.

Currently it has support for the below commands.

- LABEL
- MKDIR
- ENTRYPOINT

How to install it?

  - Download the "docker-violations-0.1.tar.gz" from "dist" directory.
  
  - Run "pip install docker-violations-0.1.tar.gz".

Docker Violations tool is installed.

How to Run it?

  python -m dockerviolations <Path of the Dockerfile in which violations to be found>
  
  Eg: python -m dockerviolations "C:\Dheeraj-PersonalData\My Git Hub Clones\docker-violations\Dockerfile"

Report Generation:

  After running the tool, report gets generated in a HTML page which gets opened automatically.
	
  This report comprises of line number(s) where the violation is present, type of violation and Recommendation.

Sample Report:
	
	![image](https://user-images.githubusercontent.com/65417565/140614555-d3579f85-d691-4e7c-b30b-e8d9ccdf3056.png)

