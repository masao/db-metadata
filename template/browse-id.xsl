<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

  <xsl:output method="html" encoding="UTF-8"/>

  <xsl:template match="/">
    <table bgcolor="#ddddd0" border="2" cellpadding="2">
      <tr>
        <td bgcolor="#aaddaa">データベースID</td>
        <td>
          <xsl:value-of select="//dbid"/>
        </td>
      </tr>
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
        <xsl:choose>
          <xsl:when test="//subfield">
            <td><xsl:value-of select="//field/@label"/>
            <a href="browse.cgi?scan=subfield;search={//field/subfield}">(<xsl:value-of select="//field/subfield"/>)</a></td>
            
          </xsl:when>
          <xsl:otherwise>
            <td><xsl:value-of select="//field/@label"/></td>

          </xsl:otherwise>
          
        </xsl:choose>
        
      </tr>
      <xsl:apply-templates select="//keyword" />
      <xsl:apply-templates select="//lang" />
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
            <xsl:when test="//user_url">
              <a><xsl:attribute name="href"><xsl:value-of select="//user_url"/></xsl:attribute><xsl:value-of select="//username"/></a>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="//usernamed"/>
            </xsl:otherwise>
          </xsl:choose>
        </td>
      </tr>
    </table>
  </xsl:template>

  <xsl:template match="//keyword">
      <tr>
        <td bgcolor="#aaddaa">キーワード</td>
        <td><a href="browse.cgi?scan=keyword;search={.}"><xsl:value-of select="."/></a></td>
      </tr>
    
  </xsl:template>
  <xsl:template match="//lang">
      <tr>
        <td bgcolor="#aaddaa">収録言語</td>
        <td><xsl:value-of select="."/></td>
      </tr>
    
  </xsl:template>
  
  <xsl:template match="*">
    <tr><td><xsl:value-of select="name(.)"/></td><td><xsl:apply-templates/></td></tr>
  </xsl:template>
</xsl:stylesheet>
