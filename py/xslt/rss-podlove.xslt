<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
	<xsl:template match="/">
			  <xsl:text disable-output-escaping="yes"><![CDATA[<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">]]></xsl:text>

		<html>
			<xsl:apply-templates/>
		</html>
	</xsl:template>
	<xsl:template match="rss">
			<xsl:apply-templates select="channel"/>
	</xsl:template>
	<xsl:template match="channel">
		<head>
			<title><xsl:value-of select="title"/></title>
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
				td#duration {
					text-align: right;
				}
				div#channel {
					margin: auto;
					margin-top: 10px;
					margin-bottom: 10px;
					width: 75%;
					border: 0px solid blue;
					padding: 15px;
					text-align: center;
				}
				div#podlove {
					margin: auto;
					width: 200px;
					border: 0px solid blue;
					padding: 15px;
				}
				div#item {
					margin: auto;
					margin-top: 10px;
					width: 40%;
					border: 3px solid green;
					padding: 10px;
				}
				a#media {
					font-weight: bold;
					color: green;
					text-decoration: none;
				}
				a#subscribe {
					font-style: bold;
					color: red;
					text-decoration: none;
				}
				font#small {
					font-size: xx-small;
					margin: 5px;
					margin-right: 20px;
				}
				font#big {
					font-size: bigger;
					margin: 5px;
					margin-left: 20px;
				}
			</style>
			<script>
				window.podcastData = {
					"title": "<xsl:value-of select='title'/>",
					"subtitle": "",
					"description": "<xsl:value-of select='description'/>",
					"cover": "<xsl:value-of select='itunes:image/@href'/>",
					"feeds": [
						{
							"type": "audio",
							"format": "mp3",
							"url": "<xsl:value-of select='atom:link/@href'/>",
							"variant": "high"
						}
					]
				}
			</script>
		</head>
		<body>
			<div id="channel">
				<h2><xsl:value-of select="title"/></h2>
			</div>
			<div id="podlove">
				<img>
					<xsl:attribute name="src"><xsl:value-of select="itunes:image/@href"/></xsl:attribute>
					<xsl:attribute name="width">200px</xsl:attribute>
				</img>
				<script class="podlove-subscribe-button"
					src="https://cdn.podlove.org/subscribe-button/javascripts/app.js"
					data-language="de" data-size="big auto" data-hide=""
					data-json-data="podcastData" data-style="filled"
					data-colors="red;green;blue">
					<xsl:comment><!-- PODLOVE Button --></xsl:comment>
				</script><br/><br/>
			</div>
			<div id="channel">
				<strong><a id="subscribe"><xsl:attribute name="href"><xsl:value-of select="atom:link/@href"/></xsl:attribute>
						Subscribe to feed (manually)</a></strong>
			</div>

			<xsl:apply-templates select="item"/>
		</body>
	</xsl:template>

	<xsl:template match="item">
		<div id="item">
			<table><tr>
				<td><font id="small">(<xsl:number/>)</font></td>
				<td width="100%">
					<a id="media">
						<xsl:attribute name="href">
							<xsl:value-of select="enclosure/@url"/>
						</xsl:attribute>
						<strong><xsl:value-of disable-output-escaping="yes" select="title"/></strong></a>
				</td><td id="duration">
					<font id="big"><xsl:value-of select="itunes:duration"/></font>
				</td>
			</tr></table>
		</div>
	</xsl:template>
</xsl:stylesheet>
