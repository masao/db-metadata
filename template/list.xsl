<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

  <xsl:output method="html" encoding="UTF-8"/>
  <xsl:param name="id"/>

  <xsl:template match="/">
    <tr valign="top">
      <td><xsl:value-of select="//id"/></td>
      <td><a href="browse.cgi?id={$id}"><xsl:value-of select="//dbname"/></a></td>
      <td>
        <xsl:choose>
          <xsl:when test="string-length(//description) > 80">
            <xsl:value-of select="substring(//description,0,80)"/>...
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="//description"/>
          </xsl:otherwise>
        </xsl:choose>

      </td>
      <td><xsl:apply-templates select="//subject" /></td>
    </tr>
  </xsl:template>
  <xsl:template match="//subject">
    <xsl:value-of select="."/>;
  </xsl:template>
</xsl:stylesheet>
