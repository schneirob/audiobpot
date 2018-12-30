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
					margin:auto;
					margin-top: 10px;
					margin-left: 20px;
				}
				div#subscribe {
					margin:auto;
					margin-top: 10px;
					margin-left: 20px;
					text-align: right;
				}
				a#subscribe {
					text-decoration: none;
					font-style: bold;
					color: red;
					font-size: x-small;
				}
				a#podlink {
					text-decoration: none;
					font-weight: bold;
					color: green;
					font-size: larger;
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
				<tr width="100%">
					<td>
						<img>
							<xsl:attribute name="src"><xsl:value-of select="image"/></xsl:attribute>
							<xsl:attribute name="width">150px</xsl:attribute>
						</img>
					</td>
					<td width="100%">
						<div id="description">
							<a id="podlink">
								<xsl:attribute name="href"><xsl:value-of select="link"/></xsl:attribute>
								<xsl:value-of select="title"/>
							</a><br/>
								(<xsl:value-of select="mediaelements"/> files,
								playtime <xsl:value-of select="duration"/>)
						</div>
						<div id="description">
							<xsl:value-of select="description"/>
						</div>

						<script>
							window.podcastData_<xsl:number/>  = {
								"title": "<xsl:value-of select='title'/>",
								"subtitle": "",
								"description": "<xsl:value-of select='description'/>",
								"cover": "<xsl:value-of select='image'/>",
								"feeds": [
									{
										"type": "audio",
										"format": "mp3",
										"url": "<xsl:value-of select='feed'/>",
										"variant": "high"
									}
								]
							}
						</script>

						<div id="description">
							<script class="podlove-subscribe-button"
								src="https://cdn.podlove.org/subscribe-button/javascripts/app.js"
								data-language="de" data-size="big" data-hide=""
								data-style="filled"
								data-colors="red;green;blue">
								<xsl:attribute name="data-json-data">podcastData_<xsl:number/></xsl:attribute>
								<xsl:comment><!-- PODLOVE Button --></xsl:comment>
							</script>
						</div>
						<div id="subscribe">
							<strong><a id="subscribe"><xsl:attribute name="href"><xsl:value-of select="feed"/></xsl:attribute>
									Subscribe to feed (manually)</a></strong>
						</div>

					</td>
				</tr>
			</table>
		</div>
	</xsl:template>
</xsl:stylesheet>
