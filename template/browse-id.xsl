<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

  <xsl:output method="html" encoding="EUC-JP"/>

  <xsl:template match="/">
    <table bgcolor="#ddddd0" border="2" cellpadding="2">
      <tr>
        <td bgcolor="#aaddaa">データベース</td>
        <td>
          <xsl:value-of select="//dbname"/>
          <xsl:if test="//dbname_yomi">
            （<xsl:value-of select="//dbname_yomi"/>）
          </xsl:if>
        </td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">データベースの特徴</td>
        <td><xsl:value-of select="//description"/></td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">分野</td>
        <td><xsl:value-of select="//field"/></td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">キーワード</td>
        <td><xsl:value-of select="//keyword"/></td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">収録言語</td>
        <td><xsl:value-of select="//lang"/></td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">収録範囲</td>
        <td><xsl:value-of select="//period"/></td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">件数</td>
        <td><xsl:value-of select="//total"/></td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">更新頻度</td>
        <td><xsl:value-of select="//interval"/></td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">更新件数</td>
        <td><xsl:value-of select="//interval_num"/></td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">システム</td>
        <td>
          <xsl:value-of select="//system"/>
          <xsl:if test="//system_yomi">
            （<xsl:value-of select="//system_yomi"/>）
          </xsl:if>
        </td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">利用料金</td>
        <td><xsl:value-of select="//fee"/></td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">利用条件</td>
        <td><xsl:value-of select="//condition"/></td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">プロデューサ</td>
        <td>
          <xsl:value-of select="//producer"/>
          <xsl:if test="//producer_yomi">
            （<xsl:value-of select="//producer_yomi"/>）
          </xsl:if>
        </td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">ディストリビュータ</td>
        <td>
          <xsl:value-of select="//distributor"/>
          <xsl:if test="//distributor_yomi">
            （<xsl:value-of select="//distributor_yomi"/>）
          </xsl:if>
        </td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">登録者</td>
        <td>
          <xsl:choose>
            <xsl:when test="//url">
              <a><xsl:attribute name="href"><xsl:value-of select="//url"/></xsl:attribute><xsl:value-of select="//企業名"/></a>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="//企業名"/>
            </xsl:otherwise>
          </xsl:choose>
        </td>
      </tr>
    </table>
  </xsl:template>

  <xsl:template match="*">
    <tr><td><xsl:value-of select="name(.)"/></td><td><xsl:apply-templates/></td></tr>
  </xsl:template>
</xsl:stylesheet>
