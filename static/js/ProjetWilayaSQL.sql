Create database ProjetWilaya
GO
use ProjetWilaya




-- Creating table 'Diplome'
CREATE TABLE [dbo].[Diplome] (
    [IdDiplome] int primary key IDENTITY(1,1),
    [DiplomeFr] nvarchar(40),
    [DiplomeAr] nvarchar(40),
    [Etablissement] nvarchar(100),
    [SpecialiteAr] nvarchar(100),
    [SpecialiteFr] nvarchar(100),
    [DateDiplome] datetime,
	[IdPersonnel#] int foreign key references [dbo].[Personnel]([IdPersonnel]),
);
GO



-- Creating table 'Division'
CREATE TABLE [dbo].[Division] (
    [IdDivision] int primary key IDENTITY(1,1),
    [LibelleDivisionAr] nvarchar(100),
    [LibelleDivisionFr] nvarchar(100)
);
GO

-- Creating table 'Service'
CREATE TABLE [dbo].[Service] (
    [IdService] int primary key IDENTITY(1,1),
    [LibelleServiceAr] nvarchar(20),
    [LibelleServiceFr] nvarchar(20),
    [IdDivision#] int foreign key references  [dbo].[Division] ([IdDivision])
);
GO
alter table Service 
ALTER COLUMN [LibelleServiceFr] nvarchar(55)
-- Creating table 'Personnel'
CREATE TABLE [dbo].[Personnel] (
    [IdPersonnel] int primary key IDENTITY(1,1),
    [NomAr] nvarchar(20),
    [PrenomAr] nvarchar(20),
    [NomFr] nvarchar(20),
    [PrenomFr] nvarchar(20),
    [Cin] nvarchar(20) UNIQUE,
    [DateNaissance] datetime,
    [LieuNaissanceAr] nvarchar(30),
	[LieuNaissanceFr] nvarchar(30),
    [AdresseAr] nvarchar(100),
    [AdresseFr] nvarchar(100),
    [Email] nvarchar(40),
    [Tele] int,
    [SituationFamilialeAr] nvarchar(40),
	[SituationFamilialeFr] nvarchar(40),
    [Sexe] nvarchar(90),
    [Vaccination] bit,
    [NumeroLocation] nvarchar(60),
    [NumeroFinancier] nvarchar(60),
    [DateRecrutement] datetime,
    [DateDemarcation] datetime,
    [DateParrainageRetraite] datetime,
    [Cmr] nvarchar(60),
    [PosteEmploye] nvarchar(60),
    [Metier] nvarchar(60),
    [TypeEmploye] nvarchar(60),
    [TachesPrecedentes] nvarchar(60),
    [Rib] int,
    [ancienneteAdmi] nvarchar(50),
    [NumCnopsAf] nvarchar(50),
    [NumCnopsIm] nvarchar(50),
    [AdministrationApp] nvarchar(50),
	[photo] nvarchar(100),
	[Age] int,
	[LastUpdate] date,
	[Statut] varchar(40),
	[Ppr] varchar(30),
);
GO

alter table Personnel
add [Statut] varchar(40);

alter table Personnel
add [Ppr] varchar(30);


-- Creating table 'Absence'
CREATE TABLE [dbo].[Absence] (
    [IdAbsence] int primary key IDENTITY(1,1),
    [DateAbsence] datetime,
	Justification bit,
    [NbJours] int,
    [Motif] nvarchar(100),
    [IdPersonnel#] int foreign key references [dbo].[Personnel]([IdPersonnel])
);
GO



-- Creating table 'Conge'
CREATE TABLE [dbo].[Conge] (
    [IdConge] int primary key IDENTITY(1,1),
    [type_conge] nvarchar(30),
    [dateDebut] datetime,
	[dateRetour] datetime,
    [nbJour] int,
    [IdPersonnel#] int foreign key references [dbo].[Personnel]([IdPersonnel])
);
GO

-- Creating table 'Stage'
CREATE TABLE [dbo].[Stage] (
    [IdStage] int primary key IDENTITY(1,1),
    [NomStagiaireAr] nvarchar(20),
    [PrenomStagiaireAr] nvarchar(20),
    [NomStagiaireFr] nvarchar(20),
    [PrenomStagiaireFr] nvarchar(20),
    [DateDebutStage] datetime,
    [DateFinStage] datetime,
    [IdService#] int foreign key references [dbo].[Service]([IdService])
);
GO


-- Creating table 'Concours'
CREATE TABLE [dbo].[Concours] (
    [IdConcours] int primary key IDENTITY(1,1),
    [LibelleConcoursAr] nvarchar(30),
	[LibelleConcoursFr] nvarchar(30),
    [DateConcours] datetime,
);
GO

-- Creating table 'Fonction'
CREATE TABLE [dbo].[Fonction] (
    [IdFonction] int primary key IDENTITY(1,1),
    [LibelleFontionAr] nvarchar(50),
    [LibelleFonctionFr] nvarchar(50)
);
GO

-- Creating table 'Position'
CREATE TABLE [dbo].[Position] (
    [IdPosition] int primary key IDENTITY(1,1),
    [LibellePositionAr] nvarchar(50),
    [LibellePositionFr] nvarchar(50),
    [LibelleSousPositionAr] nvarchar(50),
    [LibelleSousPositionFr] nvarchar(50)
);
GO

-- Creating table 'Conjoint'
CREATE TABLE [dbo].[Conjoint] (
    [IdConjoint] int primary key IDENTITY(1,1),
    [Cin] nvarchar(20),
    [NomAr] nvarchar(20),
    [NomFr] nvarchar(20),
    [PrenomAr] nvarchar(20),
    [PrenomFr] nvarchar(20),
    [DateNaissance] datetime,
    [LieuNaissance] nvarchar(20)
	[Fonction] varchar(60)
	[Ppr] varchar(30)
);
GO

alter table [dbo].[Conjoint]
add [Fonction] varchar(60);

alter table [dbo].[Conjoint]
add [Ppr] varchar(30);

-- Creating table 'Enfant'
CREATE TABLE [dbo].[Enfant] (
    [IdEnfant] int primary key IDENTITY(1,1),
    [NomAr] nvarchar(20),
    [NomFr] nvarchar(20),
    [PrenomAr] nvarchar(20),
    [PrenomFr] nvarchar(20),
    [DateNaissance] datetime,
    [LieuNaissanceAr] nvarchar(20),
	[LieuNaissanceFr] nvarchar(20),
    [LienJuridique] nvarchar(30),
    [IdConjoint#] int foreign key references [dbo].[Conjoint]([IdConjoint])
);
GO
drop table Echelle
-- Creating table 'Echelle'
CREATE TABLE [dbo].[Echelle] (
    [IdEchelle] int primary key IDENTITY(1,1),
    [Echelle] nvarchar(15),
);
GO


-- Creating table 'Echellon'
CREATE TABLE [dbo].[Echellon] (
    [IdEchellon] int primary key IDENTITY(1,1),
    [Echellon] nvarchar(30),
);
GO
-- Creating table 'StatutGrade'
CREATE TABLE [dbo].[StatutGrade](
[idStatutGrade] int  primary key IDENTITY(1,1),
[StatutGradeFr] nvarchar(30),
[StatutGradeAr] nvarchar(30),
)


-- Creating table 'Grade'
CREATE TABLE [dbo].[Grade] (
    [IdGrade] int primary key IDENTITY(1,1),
    [GradeAr] nvarchar(55),
    [GradeFr] nvarchar(55),
	idStatutGrade# int foreign key references StatutGrade(idStatutGrade),
	idEchelle# int foreign key references Echelle(idEchelle),
);
GO

-- Creating table 'GradePersonnel'
CREATE TABLE [dbo].[GradePersonnel] (
	[IdGradePersonnel] int primary key identity(1,1),
    [IdGrade#] int foreign key references [dbo].[Grade]([IdGrade]),
    [IdPersonnel#] int foreign key references [dbo].[Personnel]([IdPersonnel]),
    [DateGrade] datetime,
    [ChangementDeGrade] nvarchar(100),
	idEchellon# int foreign key references Echellon(idEchellon),
	[Indice] nvarchar(15),
	[DateEchellon] datetime,
	[ChangementDEchellon] nvarchar(100),
);
GO
SET IDENTITY_INSERT GradePersonnel OFF
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (20,1,159,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (2,2,158,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (3,3,157,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (4,4,156,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (5,4,155,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (6,5,154,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (7,6,153,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (8,6,152,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (9,7,151,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (10,7,150,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (11,8,149,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (12,9,148,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (13,9,147,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (14,10,146,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (15,11,145,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (16,12,144,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (17,13,143,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (18,14,142,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (19,15,141,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (20,16,139,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (21,17,138,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (22,18,137,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')
insert into GradePersonnel(IdGradePersonnel,IdGrade#,IdPersonnel#,DateGrade,ChangementDeGrade,idEchellon#,Indice,DateEchellon,ChangementDEchellon) values (23,19,136,'2020-05-05','Ancienté',5,'736','2020-05-05','Concour')




-- Creating table 'ServicePersonnel'
CREATE TABLE [dbo].[ServicePersonnel] (
    
	[IdServicePersonnel] int primary key identity(1,1),
    [IdService#] int foreign key references [dbo].[Service]([IdService]),
	[IdPersonnel#] int foreign key references [dbo].[Personnel]([IdPersonnel]),
    [DateAffectation] datetime,
    
);
GO

-- Creating table 'FonctionPersonnel'
CREATE TABLE [dbo].[FonctionPersonnel] (
    [IdFonctionPersonnel] int primary key identity(1,1),
    [IdFonction#] int foreign key references [dbo].[Fonction]([IdFonction]),
	[IdPersonnel#] int foreign key references [dbo].[Personnel]([IdPersonnel]),
    [DateFonction] datetime,
);
GO

-- Creating table 'ThematiqueFormation'
CREATE TABLE [dbo].[ThematiqueFormation] (
    [IdThematiqueFormation] int primary key IDENTITY(1,1),
    [LibelleThematique] nvarchar(70)
);
GO


-- Creating table 'ThematiqueFormationPersonnel'
CREATE TABLE [dbo].[ThematiqueFormationPersonnel] (
    [IdThematiqueFormation#] int foreign key references [dbo].[ThematiqueFormation]([IdThematiqueFormation]),
    [IdPersonnel#] int foreign key references [dbo].[Personnel]([IdPersonnel]),
    [Date] datetime,
    [Duree] int,
    [Presence] bit,
	primary key([IdThematiqueFormation#],[IdPersonnel#])

    
);
GO

-- Creating table 'PositionPersonnel'
CREATE TABLE [dbo].[PositionPersonnel] (
    [IdPosition#] int foreign key references [dbo].[Position]([IdPosition]),
    [IdPersonnel#] int foreign key references [dbo].[Personnel]([IdPersonnel]),
	primary key([IdPosition#], [IdPersonnel#])
);
GO

-- Creating table 'ConjointPersonnel'
CREATE TABLE [dbo].[ConjointPersonnel] (
    [IdConjoint#] int foreign key references [dbo].[Conjoint]([IdConjoint]),
    [IdPersonnel#] int foreign key references [dbo].[Personnel]([IdPersonnel]),
	primary key([IdConjoint#],[IdPersonnel#])
);
GO

CREATE TABLE [dbo].[DateElimine](
	[IdDateElimine] int primary key identity(1,1),
	[Motif] nvarchar(50),
	DateElimine datetime,
	)
GO


select d.LibelleDivisionAr,d.LibelleDivisionFr, count(c.IdConge) as total 
from [dbo].[Division] d inner join [dbo].[Service] s on s.IdDivision# = d.IdDivision 
inner join [dbo].[ServicePersonnel] sp on s.IdService = sp.IdService# 
inner join [dbo].[Personnel] p on sp.IdPersonnel# = p.IdPersonnel 
inner join [dbo].[Conge] c on p.IdPersonnel = c.IdPersonnel# 
group by d.LibelleDivisionAr,d.LibelleDivisionFr,d.IdDivision
