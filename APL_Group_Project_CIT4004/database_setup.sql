USE master
GO

IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'APLProjectDB')
BEGIN
  CREATE DATABASE APLProjectDB;
END;
GO

USE APLProjectDB
GO

---=======================================================================================================
IF (EXISTS (SELECT * 
                 FROM INFORMATION_SCHEMA.TABLES 
                 WHERE TABLE_SCHEMA = 'dbo' 
                 AND  TABLE_NAME = 'Reservations'))
BEGIN
    DROP TABLE dbo.Reservations
END

CREATE TABLE Reservations (
    ID INT IDENTITY(1,1),
    ClientName varchar(255),
    Place varchar(255),
    [StartDate] date,
	[EndDate] date,
    [Location] varchar(255),
	[Destination] varchar(255),
	[Status] VARCHAR(12),
	[IsPaid] Bit,
	CreatedDateTime DateTime
);
GO


---=======================================================================================================
IF (EXISTS (SELECT * 
                 FROM INFORMATION_SCHEMA.TABLES 
                 WHERE TABLE_SCHEMA = 'dbo' 
                 AND  TABLE_NAME = 'TicketBookings'))
BEGIN
    DROP TABLE dbo.TicketBookings
END

CREATE TABLE TicketBookings (
    ID INT IDENTITY(1,1),
    ClientName varchar(255),
    Place varchar(255),
    [StartDate] date,
	[EndDate] date,
    [Location] varchar(255),
	[Destination] varchar(255),
	[Status] VARCHAR(12),
	CreatedDateTime DateTime
);
GO

---=======================================================================================================
IF EXISTS ( SELECT * 
            FROM   sysobjects 
            WHERE  id = object_id(N'[dbo].[Create_New_TicketBooking]'))
BEGIN
    DROP PROCEDURE [dbo].[Create_New_TicketBooking]
END
GO

CREATE PROCEDURE Create_New_TicketBooking 
	@Client_Name nvarchar(255) = NULL,
	@Place	   nvarchar(255) = NULL,
	@Start_Date Varchar(12) = NULL,
	@End_Date Varchar(12) = NULL,
	@Location nvarchar(255) = NULL,
	@Destination nvarchar(255) = NULL
AS
BEGIN
	INSERT INTO TicketBookings
	(ClientName, Place, StartDate, EndDate, [Location], Destination, [Status], CreatedDateTime)
	VALUES
	(@Client_Name, @Place, @Start_Date, @End_Date, @Location, @Destination, 'Active', GETDATE())
END
GO

---=======================================================================================================
IF EXISTS ( SELECT * 
            FROM   sysobjects 
            WHERE  id = object_id(N'[dbo].[Create_New_Reservation]'))
BEGIN
    DROP PROCEDURE [dbo].[Create_New_Reservation]
END
GO

CREATE PROCEDURE Create_New_Reservation 
	@Client_Name nvarchar(255) = NULL,
	@Place	   nvarchar(255) = NULL,
	@Start_Date Varchar(12) = NULL,
	@End_Date Varchar(12) = NULL,
	@Location nvarchar(255) = NULL,
	@Destination nvarchar(255) = NULL
AS
BEGIN
	INSERT INTO Reservations
	(ClientName, Place, StartDate, EndDate, [Location], Destination, [Status], IsPaid, CreatedDateTime)
	VALUES
	(@Client_Name, @Place, @Start_Date, @End_Date, @Location, @Destination, 'Active', 0, GETDATE())
END
GO


---=======================================================================================================
IF EXISTS ( SELECT * 
            FROM   sysobjects 
            WHERE  id = object_id(N'[dbo].[Cancel_Active_Reservation]'))
BEGIN
    DROP PROCEDURE [dbo].[Cancel_Active_Reservation]
END
GO

CREATE PROCEDURE Cancel_Active_Reservation 
	@Client_Name nvarchar(255) = NULL,
	@Place	   nvarchar(255) = NULL,
	@Reservation_No varchar(255) = NULL
AS
BEGIN
	IF @Reservation_No = '' OR @Reservation_No = 'none'
		SET @Reservation_No = NULL

	IF @Client_Name = '' OR @Client_Name = 'none'
		SET @Client_Name = NULL

	IF @Reservation_No IS NOT NULL AND @Client_Name IS NOT NULL
	BEGIN
		UPDATE Reservations
		SET [Status] = 'Cancelled'
		WHERE ID = CAST(@Reservation_No AS INT) AND ClientName = @Client_Name
	END

	IF @Client_Name IS NOT NULL AND @Reservation_No IS NULL
	BEGIN
		UPDATE Reservations
		SET [Status] = 'Cancelled'
		WHERE ClientName = @Client_Name
	END
END
GO


---=======================================================================================================
IF EXISTS ( SELECT * 
            FROM   sysobjects 
            WHERE  id = object_id(N'[dbo].[Confirm_Client_Reservation]'))
BEGIN
    DROP PROCEDURE [dbo].[Confirm_Client_Reservation]
END
GO

CREATE PROCEDURE Confirm_Client_Reservation 
	@Client_Name nvarchar(255) = NULL,
	@Place	   nvarchar(255) = NULL,
	@Reservation_No Varchar = NULL
AS
BEGIN
	IF @Reservation_No = '' OR @Reservation_No = 'none'
		SET @Reservation_No = NULL

	IF @Client_Name = '' OR @Client_Name = 'none'
		SET @Client_Name = NULL

	IF @Reservation_No IS NOT NULL AND @Client_Name IS NOT NULL
	BEGIN
		UPDATE Reservations
		SET [Status] = 'Confirmed'
		WHERE ID = CAST(@Reservation_No AS INT) AND ClientName = @Client_Name
	END

	IF @Client_Name IS NOT NULL AND @Reservation_No IS NULL
	BEGIN
		UPDATE Reservations
		SET [Status] = 'Confirmed'
		WHERE ClientName = @Client_Name
	END
END
GO


---=======================================================================================================
IF EXISTS ( SELECT * 
            FROM   sysobjects 
            WHERE  id = object_id(N'[dbo].[Pay_Client_Reservation]'))
BEGIN
    DROP PROCEDURE [dbo].[Pay_Client_Reservation]
END
GO

CREATE PROCEDURE Pay_Client_Reservation 
	@Client_Name nvarchar(255) = NULL,
	@Place	   nvarchar(255) = NULL,
	@Reservation_No Varchar = NULL
AS
BEGIN
	IF @Reservation_No = '' OR @Reservation_No = 'none'
		SET @Reservation_No = NULL

	IF @Client_Name = '' OR @Client_Name = 'none'
		SET @Client_Name = NULL

	IF @Reservation_No IS NOT NULL AND @Client_Name IS NOT NULL
	BEGIN
		UPDATE Reservations
		SET [Status] = 'PAID', IsPaid = 1
		WHERE ID = CAST(@Reservation_No AS INT) AND ClientName = @Client_Name
	END

	IF @Client_Name IS NOT NULL AND @Reservation_No IS NULL
	BEGIN
		UPDATE Reservations
		SET [Status] = 'Paid', IsPaid = 1
		WHERE ClientName = @Client_Name
	END
END
GO


---=======================================================================================================
IF EXISTS ( SELECT * 
            FROM   sysobjects 
            WHERE  id = object_id(N'[dbo].[Cancel_TicketBooking_For_Client]'))
BEGIN
    DROP PROCEDURE [dbo].[Cancel_TicketBooking_For_Client]
END
GO

CREATE PROCEDURE Cancel_TicketBooking_For_Client 
	@Client_Name nvarchar(255) = NULL,
	@Place	   nvarchar(255) = NULL,
	@Ticket_No varchar(255) = NULL
AS
BEGIN
	IF @Ticket_No = '' OR @Ticket_No = 'none'
		SET @Ticket_No = NULL

	IF @Client_Name = '' OR @Client_Name = 'none'
		SET @Client_Name = NULL

	IF @Ticket_No IS NOT NULL AND @Client_Name IS NOT NULL
	BEGIN
		UPDATE TicketBookings
		SET [Status] = 'Cancelled'
		WHERE ID = CAST(@Ticket_No AS INT) AND ClientName = @Client_Name
	END

	IF @Client_Name IS NOT NULL AND @Ticket_No IS NULL
	BEGIN
		UPDATE TicketBookings
		SET [Status] = 'Cancelled'
		WHERE ClientName = @Client_Name
	END
END
GO



---=======================================================================================================
---Create user for accessing the database from the application
---=======================================================================================================

USE [master]
GO

/* For security reasons the login is created disabled and with a random password. */
/****** Object:  Login [apl]    Script Date: 3/30/2025 3:46:28 PM ******/

--Check if the user already exists
IF  EXISTS (SELECT * FROM sys.database_principals WHERE name = N'apl')
DROP USER [apl]
GO

CREATE LOGIN [apl] WITH PASSWORD=N'DLaMs2QDWItWCU9Rk9bj5kUsi3D1JxJDHjONUSClM6Q=', DEFAULT_DATABASE=[master], DEFAULT_LANGUAGE=[us_english], CHECK_EXPIRATION=OFF, CHECK_POLICY=OFF
GO

ALTER SERVER ROLE [sysadmin] ADD MEMBER [apl]
GO

