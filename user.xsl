<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

  <xsl:output method="text"/>

  <xsl:template match="/">
    <xsl:value-of select="//企業NO."/>:*:<xsl:value-of select="//企業名"/>&lt;&gt;<xsl:value-of select="//企業種別"/>&lt;&gt;<xsl:value-of select="//コメント"/>&lt;&gt;<xsl:if test="//URL!='-'"><xsl:value-of select="//URL"/></xsl:if><xsl:text>
</xsl:text>
  </xsl:template>

</xsl:stylesheet>
