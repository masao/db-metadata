<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

  <xsl:output method="html" encoding="EUC-JP"/>
  <xsl:param name="id"/>

  <xsl:template match="/">
    <tr valign="top">
      <td><xsl:value-of select="//dbid"/></td>
      <td><a href="browse.cgi?id={$id}"><xsl:value-of select="//dbname"/></a></td>
      <td><xsl:value-of select="//description"/></td>
      <td><xsl:value-of select="//field"/></td>
    </tr>
  </xsl:template>
</xsl:stylesheet>
