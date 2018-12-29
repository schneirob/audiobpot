<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
	<xsl:template match="/">
			  <xsl:text disable-output-escaping="yes"><![CDATA[<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">]]></xsl:text>

		<html>
			<xsl:apply-templates/>
		</html>
	</xsl:template>
	<xsl:template match="rss">
		<head>
			<title><xsl:value-of select="./channel/title"/></title>
			<style>
				html * {
					font-family: Arial, Helvetica, Sans-Serif !important;
				}
				table, tr, td, th {
					border: 0px solid black;
				}
				td {
					padding: 2px;
					border-spacing: 2px;
				}
				td#keyword {
					font-weight: bold;
					text-align: right;
				}
				div#channel {
					margin: auto;
					width: 75%;
					border: 3px solid red;
					padding: 10px;
				}
				div#item {
					margin: auto;
					margin-top: 10px;
					width: 60%;
					border: 3px solid green;
					padding: 10px;
				}
				div#item_media {
					margin-top: 10px;
					margin-left: 20px;
				}
				div#item_description {
					margin-top: 10px;
					margin-left: 20px;
				}
				div#item_subtitle {
					margin:auto;
					text-align: center;
					font-style: italic;
					margin-top: -5px;
				}
			</style>
		</head>
		<body>
			<xsl:apply-templates select="channel"/>
		</body>
	</xsl:template>
	<xsl:template match="channel">
		<div id="channel">
			<table>
				<tr>
					<xsl:if test="itunes:image/@href">
						<td rowspan="6">
							<img>
								<xsl:attribute name="src">
									<xsl:value-of select="itunes:image/@href"/>
								</xsl:attribute>
								<xsl:attribute name="width">
									200px
								</xsl:attribute>
							</img>
						</td>
					</xsl:if>
					<td id="keyword">Title : </td>
					<td><xsl:value-of select="title"/></td>
				</tr>
				<tr>
					<td id="keyword">Page link : </td>
					<td>
						<a>
							<xsl:attribute name="href">
								<xsl:value-of select="link"/>
							</xsl:attribute>
							<xsl:value-of select="link"/>
						</a>
					</td>
				</tr>
				<tr>
					<td id="keyword">Feed link : </td>
					<td>
						<a>
							<xsl:attribute name="href">
								<xsl:value-of select="atom:link/@href"/>
							</xsl:attribute>
							<xsl:value-of select="atom:link/@href"/>
						</a>
					</td>
				</tr>
				<tr>
					<td id="keyword">Last build date : </td>
					<td><xsl:value-of select="lastBuildDate"/></td>
				</tr>
				<tr>
					<td id="keyword">Publication date : </td>
					<td><xsl:value-of select="pubDate"/></td>
				</tr>
				<tr>
					<td id="keyword">Description : </td>
					<td><xsl:value-of select="description"/></td>
				</tr>
			</table>
		</div>
		<xsl:apply-templates select="item"/>
	</xsl:template>
	<xsl:template match="item">
		<div id="item">
			<h3 id="title">
				<xsl:value-of disable-output-escaping="yes" select="title"/>(<xsl:value-of select="itunes:duration"/>)
			</h3>
			<div id="item_subtitle">
				<xsl:value-of disable-output-escaping="yes" select="itunes:subtitle"/><br/>
				(<xsl:value-of select="pubDate"/>)
			</div>
			<div id="item_media">
				<a>
					<xsl:attribute name="href">
						<xsl:value-of select="enclosure/@url"/>
					</xsl:attribute>
					<xsl:value-of select="enclosure/@url"/>
				</a><br/>
				(<xsl:value-of select="enclosure/@type"/>,
				<xsl:value-of select="enclosure/@length"/> byte)
			</div>
			<div id="item_description">
				<xsl:value-of disable-output-escaping="yes" select="description"/>
			</div>
		</div>
	</xsl:template>
</xsl:stylesheet>
