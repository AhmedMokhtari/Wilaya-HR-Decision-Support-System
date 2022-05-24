alter table Caidat
alter column [LibelleCaidatAr] nvarchar(100)
go
alter table Caidat    
alter column [LibelleCaidatFr] nvarchar(100)
go

alter table Annexe    
alter column [LibelleAnnexeAr] nvarchar(100)
go

alter table Annexe
alter column [LibelleAnnexeFr] nvarchar(100)
go

SET IDENTITY_INSERT Entite ON
GO

-- Insert Entite	
insert into Entite (IdEntite,LibelleEntitenAr,LibelleEntiteFr) values (1,N'الدوائر الحضرية','Commandement')
GO

SET IDENTITY_INSERT Entite OFF
GO

SET IDENTITY_INSERT District ON
GO

insert into District (IdDistrict,LibelleDistrictAr,LibelleDistrictFr,IdEntite#) values (1,N'المنطقة الحضرية وجدة سيدي زيان','District Urbain Oujda Sidi Ziane',1)
insert into District (IdDistrict,LibelleDistrictAr,LibelleDistrictFr,IdEntite#) values (2,N'المنطقة الحضرية سيدي ادريس القاضي','District Urbain Sidi Driss El Qadi',1)
insert into District (IdDistrict,LibelleDistrictAr,LibelleDistrictFr,IdEntite#) values (3,N'المنطقة الحضرية واد الناشف سيدي معافة','District Urbain Oued Ennachef Sidi Maafa',1)
insert into District (IdDistrict,LibelleDistrictAr,LibelleDistrictFr,IdEntite#) values (4,N'المنطقة الحضرية سيدي يحي','District Urbain Sidi Yahya',1)
Go

SET IDENTITY_INSERT District OFF
GO

-- Insert Pachalik

SET IDENTITY_INSERT Pashalik ON
GO

insert into Pashalik (IdPashalik,LibellePashalikAr,LibellePashalikFr,IdEntite#) values (1,N'باشوية وجدة','Pachalik Oujda',1)
insert into Pashalik (IdPashalik,LibellePashalikAr,LibellePashalikFr,IdEntite#) values (2,N'باشوية بني ادرار','Pachalik Bni Drar',1)
insert into Pashalik (IdPashalik,LibellePashalikAr,LibellePashalikFr,IdEntite#) values (3,N'باشوية النعيمة','Pachalik Naima',1)
GO

SET IDENTITY_INSERT Pashalik OFF
GO

-- Insert Annexe

SET IDENTITY_INSERT Annexe ON
go

insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (1,N'مقر المنطقة الحضرية وجدة سيدي زيان','Lieu District Urbain Oujda Sidi Ziane',1)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (2,N'الملحقة الإدارية الأولى','1ère  Annexe Administrative',1)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (3,N'الملحقة الإدارية الثانية','2ème Annexe Administrative',1)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (4,N'الملحقة الإدارية ابثالثة','3ème Annexe Administrative',1)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (5,N'الملحقة الإدارية الرابعة','4ème Annexe Administrative',1)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (6,N'مقر المنطقة الحضرية سيدي ادريس القاضي','Lieu District Urbain Sidi Driss El Qadi',2)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (7,N'الملحقة الإدارية الخامسة','5ème Annexe Administrative',2)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (8,N'الملحقة الإدارية السادسة','6ème Annexe Administrative',2)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (9,N'الملحقة الإدارية السابعة','7ème Annexe Administrative',2)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (10,N'الملحقة الإدارية الثامنة','8ème Annexe Administrative',2)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (11,N'مقر المنطقة الحضرية واد الناشف سيدي معافة','Lieu District Urbain Oued Ennachef Sidi Maafa',3)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (12,N'الملحقة الإدارية التاسعة','9ème Annexe Administrative',3)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (13,N'الملحقة الإدارية العاشرة','10ème Annexe Administrative',3)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (14,N'الملحقة الإدارية الحادية عشر','11ème Annexe Administrative',3)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (15,N'الملحقة الإدارية الثانية عشر','12ème Annexe Administrative',3)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (16,N'الملحقة الإدارية السادسة عشر','16ème Annexe Administrative',3)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (17,N'الملحقة الإدارية السابعة عشر','17ème Annexe Administrative',3)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (18,N'مقر المنطقة الحضرية سيدي يحي','Lieu District Urbain Sidi Yahya',4)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (19,N'الملحقة الإدارية الثالثة عشر','13ème Annexe Administrative',4)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (20,N'الملحقة الإدارية الرابعة عشر','14ème Annexe Administrative',4)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (21,N'الملحقة الإدارية الخامسة عشر','15ème Annexe Administrative',4)
insert into Annexe(IdAnnexe,LibelleAnnexeAr,LibelleAnnexeFr,IdDistrict#) values (22,N'الملحقة الإدارية الثامنة عشر','18ème Annexe Administrative',4)
go

SET IDENTITY_INSERT Annexe OFF
go

-- Insert Cercle

SET IDENTITY_INSERT Cercle ON
go

insert into Cercle (IdCercle,LibelleCercleAr,LibelleCercleFr,IdEntite#) values(1,N'دائرة أحواز وجدة الشمالية','Cercle Oujda Banlieue Nord',1)
insert into Cercle (IdCercle,LibelleCercleAr,LibelleCercleFr,IdEntite#) values(2,N'دائرة أحواز وجدة الجنوبية','Cercle Oujda Banlieue Sud',1)
go

SET IDENTITY_INSERT Cercle OFF
go

-- Insert Caidat

SET IDENTITY_INSERT Caidat ON
go

insert into Caidat(IdCaidat,LibelleCaidatAr,LibelleCaidatFr,IdCercle#) values (1,N'مقر دائرة أحواز وجدة الشمالية','Lieu Cercle Oujda Banlieue Nord',1)
insert into Caidat(IdCaidat,LibelleCaidatAr,LibelleCaidatFr,IdCercle#) values (2,N'قيادة أنكاد','Caidat Angad',1)
insert into Caidat(IdCaidat,LibelleCaidatAr,LibelleCaidatFr,IdCercle#) values (3,N'قيادة بني خالد','Caidat Bni khaled',1)
insert into Caidat(IdCaidat,LibelleCaidatAr,LibelleCaidatFr,IdCercle#) values (4,N'قيادة عين الصفا','Caidat Ain Sfa',1)
insert into Caidat(IdCaidat,LibelleCaidatAr,LibelleCaidatFr,IdCercle#) values (5,N'مقر دائرة أحواز وجدة الجنوبية','Lieu Cercle Oujda Banlieue Sud',2)
insert into Caidat(IdCaidat,LibelleCaidatAr,LibelleCaidatFr,IdCercle#) values (6,N'قيادة إسلي بني وكيل','Caidat Isly Bni Oukil',2)
insert into Caidat(IdCaidat,LibelleCaidatAr,LibelleCaidatFr,IdCercle#) values (7,N'قيادة واد إسلي','Caidat Oued Isly',2)
go

SET IDENTITY_INSERT Caidat OFF
go



