CREATE DATABASE [ChessAIProject] 
USE [ChessAIProject]
GO
/****** Object:  Table [dbo].[level]    Script Date: 12/12/2022 9:35:33 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[level](
	[id_level] [int] NOT NULL,
	[level_name] [varchar](50) NULL,
	[detail] [varchar](50) NULL,
 CONSTRAINT [PK_level] PRIMARY KEY CLUSTERED 
(
	[id_level] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[match_history]    Script Date: 12/12/2022 9:35:33 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/****** Object:  Table [dbo].[player]    Script Date: 12/12/2022 9:35:33 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[player](
	[username] [varchar](50) NOT NULL,
	[password] [varchar](50) NULL,
	[fullname] [varchar](100) NULL,
	[id_level] [int] NOT NULL,
 CONSTRAINT [PK_player] PRIMARY KEY CLUSTERED 
(
	[username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[player]  WITH CHECK ADD  CONSTRAINT [FK_player_level] FOREIGN KEY([id_level])
REFERENCES [dbo].[level] ([id_level])
GO
USE [master]
GO
ALTER DATABASE [ChessAIProject] SET  READ_WRITE 
GO