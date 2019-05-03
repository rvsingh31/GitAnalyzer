CREATE TABLE "Repos" (
	"RepoId" serial NOT NULL,
	"RepoName" TEXT NOT NULL,
	"RepoUrl" TEXT NOT NULL UNIQUE,
	CONSTRAINT Repos_pk PRIMARY KEY ("RepoId")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Files" (
	"FileId" serial NOT NULL,
	"RepoId" serial NOT NULL,
	"FileName" TEXT NOT NULL,
	"FilePath" TEXT NOT NULL,
	"FileType" TEXT NOT NULL,
	"LastModified" DATETIME NOT NULL,
	"FileSizeBytes" FLOAT NOT NULL,
	"LinesOfCode" integer NOT NULL,
	CONSTRAINT Files_pk PRIMARY KEY ("FileId")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "SubjectExperts" (
	"FileId" integer NOT NULL,
	"AuthorId" integer NOT NULL,
	"Score" integer NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Authors" (
	"AuthorId" serial NOT NULL,
	"AuthorName" TEXT NOT NULL,
	"AuthorEmail" TEXT NOT NULL,
	CONSTRAINT Authors_pk PRIMARY KEY ("AuthorId")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "FileDependencies " (
	"SouceFileId" integer NOT NULL,
	"DestinationFileId" integer NOT NULL,
	"NoOfTimeChanged" integer NOT NULL,
	"NormalizedChanged" FLOAT NOT NULL
) WITH (
  OIDS=FALSE
);



CREATE TABLE "BugProbabilities" (
	"FileId" integer NOT NULL,
	"NoOfTimeChanged" integer NOT NULL,
	"BuggyCommits" integer NOT NULL,
	"BuggyCommitsPercentage" FLOAT NOT NULL
) WITH (
  OIDS=FALSE
);




ALTER TABLE "Files" ADD CONSTRAINT "Files_fk0" FOREIGN KEY ("RepoId") REFERENCES "Repos"("RepoId");

ALTER TABLE "SubjectExperts" ADD CONSTRAINT "SubjectExperts_fk0" FOREIGN KEY ("FileId") REFERENCES "Files"("FileId");
ALTER TABLE "SubjectExperts" ADD CONSTRAINT "SubjectExperts_fk1" FOREIGN KEY ("AuthorId") REFERENCES "Authors"("AuthorId");


ALTER TABLE "FileDependencies " ADD CONSTRAINT "FileDependencies _fk0" FOREIGN KEY ("SouceFileId") REFERENCES "Files"("FileId");
ALTER TABLE "FileDependencies " ADD CONSTRAINT "FileDependencies _fk1" FOREIGN KEY ("DestinationFileId") REFERENCES "Files"("FileId");

ALTER TABLE "BugProbabilities" ADD CONSTRAINT "BugProbabilities_fk0" FOREIGN KEY ("FileId") REFERENCES "Files"("FileId");

