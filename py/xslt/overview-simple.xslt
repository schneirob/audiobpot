<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
			  <xsl:text disable-output-escaping="yes"><![CDATA[<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">]]></xsl:text>
		<html>
			<xsl:apply-templates/>
		</html>
	</xsl:template>
	<xsl:template match="podcastlist">
		<head>
			<title>AutoBPot Podcast Overview</title>
			<style>
				html * {
					font-family: Arial, Helvetica, Sans-Serif !important;
				}
				table, tr, td, th {
					border: 0px solid black;
				}
				td {
					padding: 10px;
					border-spacing: 10px;
				}
				div#podcast {
					margin: auto;
					margin-top: 10px;
					width: 60%;
					border: 3px solid green;
					padding: 10px;
				}
				div#description {
					margin-top: 10px;
					margin-left: 20px;
				}
			</style>
		</head>
		<body>
			<xsl:apply-templates select="podcast"/>
		</body>
	</xsl:template>
	<xsl:template match="podcast">
		<div id="podcast">
			<table>
				<tr>
					<xsl:if test="image">
						<td>
							<img>
								<xsl:attribute name="src">
									<xsl:value-of select="image"/>
								</xsl:attribute>
								<xsl:attribute name="width">
									100px
								</xsl:attribute>
							</img>
						</td>
					</xsl:if>
					<td>
						<h3 id="title">
							<xsl:value-of select="title"/>
							(<xsl:value-of select="mediaelements"/> files,
							playtime <xsl:value-of select="duration"/>)
						</h3>
						<div id="description">
							<xsl:value-of select="description"/>
						</div>
						<div id="description">
							<strong>Feed: </strong>
							<a>
								<xsl:attribute name="href">
									<xsl:value-of select="feed"/>
								</xsl:attribute>
								<xsl:value-of select="feed"/>
							</a><br/>
							<strong>Website: </strong>
							<a>
								<xsl:attribute name="href">
									<xsl:value-of select="link"/>
								</xsl:attribute>
								<xsl:value-of select="link"/>
							</a><br/>
						</div>
					</td>
				</tr>
			</table>
		</div>
	</xsl:template>
</xsl:stylesheet>
