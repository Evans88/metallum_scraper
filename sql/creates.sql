 CREATE TABLE band(
	 Id varchar(50) primary key not null
	,[Name] nvarchar(102)
	,[Country of Origin] nvarchar(75)
	,[Location] nvarchar(150)
	,[Status] varchar(25)
	,[Year Formed] varchar(10)
	,[Genre] varchar(150)
	,[Lyrical Themes] varchar(150)
	,[Current Label] varchar(150)
	,[Years Active] varchar(200)
	,datetime_added datetime
	,datetime_modified datetime
)

 CREATE TABLE album(
	 Id varchar(50) primary key not null
	,[Band Id] varchar(50) not null
	,[Name] nvarchar(102)
	,[Type] nvarchar(50)
	,[Release Date] nvarchar(150)
	,[Catalog Id] varchar(125)
	,[Label] varchar(150)
	,[Format] varchar(50)
	,[Review Count] int
	,[Average Review] float(2)
	,datetime_added datetime
	,datetime_modified datetime
)