<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

  <xsl:output method="html" encoding="EUC-JP"/>

  <xsl:template match="/">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="*">
    <ul><li><xsl:value-of select="name(.)"/>: <xsl:apply-templates/></li></ul>
  </xsl:template>
</xsl:stylesheet>
