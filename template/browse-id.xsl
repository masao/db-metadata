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
          <a href="browse.cgi?scan=dbname;search={//dbname}"><xsl:value-of select="//dbname"/></a>
          <xsl:if test="//dbname_yomi and boolean(string-length(//dbname_yomi))">
            （<xsl:value-of select="//dbname_yomi"/>）
          </xsl:if>
        </td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">データベースの特徴</td>
        <td><xsl:value-of select="//description"/></td>
      </tr>
      <xsl:apply-templates select="//field" />
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
          <a href="browse.cgi?scan=system;search={//system}">
          <xsl:value-of select="//system"/></a>
          <xsl:if test="//system_yomi and boolean(string-length(//system_yomi))">
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
          <a href="browse.cgi?scan=producer;search={//producer}">
            <xsl:value-of select="//producer"/></a>
          <xsl:if test="//producer_yomi and boolean(string-length(//producer_yomi))">
            （<xsl:value-of select="//producer_yomi"/>）
          </xsl:if>
        </td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">ディストリビュータ</td>
        <td>
          <a href="browse.cgi?scan=distributor;search={//distributor}">
            <xsl:value-of select="//distributor"/></a>
          <xsl:if test="//distributor_yomi and boolean(string-length(//distributor_yomi))">
            （<xsl:value-of select="//distributor_yomi"/>）
          </xsl:if>
        </td>
      </tr>
      <!--
      <tr>
        <td bgcolor="#aaddaa">登録者</td>
        <td>
          <a href="browse.cgi?scan=username;search={//username}"><xsl:value-of select="//username"/></a>
          <xsl:if test="//user_url">
            (<a><xsl:attribute name="href"><xsl:value-of select="//user_url"/></xsl:attribute><xsl:value-of select="//user_url"/></a>)
          </xsl:if>
        </td>
      </tr>
      -->
    </table>
  </xsl:template>

  <xsl:template match="//field">
      <tr>
        <td bgcolor="#aaddaa">分野</td>
        <td><xsl:value-of select="@label"/>
        <a href="browse.cgi?scan=field;search={.}">(<xsl:value-of select="."/>)</a></td>
        
      </tr>
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
