<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

  <xsl:output method="html" encoding="UTF-8"/>

  <xsl:template match="/">
    <table bgcolor="#ddddd0" border="2" cellpadding="2">
      <tr>
        <td bgcolor="#aaddaa">データベースID</td>
        <td>
          <xsl:value-of select="//id"/>
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
      <xsl:if test="boolean(string-length(//description))">
        <tr>
          <td bgcolor="#aaddaa">データベースの特徴</td>
          <td><xsl:value-of select="//description"/></td>
        </tr>
      </xsl:if>
      <xsl:if test="boolean(string-length(//subject))">
        <xsl:apply-templates select="//subject" />
      </xsl:if>
      <xsl:if test="boolean(string-length(//lang))">
        <xsl:apply-templates select="//lang" />
      </xsl:if>
      <xsl:if test="boolean(string-length(//period))">
        <tr>
          <td bgcolor="#aaddaa">収録期間</td>
          <td><xsl:value-of select="//period"/></td>
        </tr>
      </xsl:if>
      <xsl:if test="boolean(string-length(//total))">
        <tr>
          <td bgcolor="#aaddaa">収録件数</td>
          <td><xsl:value-of select="//total"/></td>
        </tr>
      </xsl:if>
      <xsl:if test="boolean(string-length(//interval))">
        <tr>
          <td bgcolor="#aaddaa">更新頻度</td>
          <td><xsl:value-of select="//interval"/></td>
        </tr>
      </xsl:if>
      <xsl:if test="boolean(string-length(//interval_num))">
        <tr>
          <td bgcolor="#aaddaa">更新件数</td>
          <td><xsl:value-of select="//interval_num"/></td>
        </tr>
      </xsl:if>
      <xsl:if test="boolean(string-length(//region))">
        <tr>
          <td bgcolor="#aaddaa">収録情報の地域</td>
          <td><xsl:value-of select="//region"/></td>
        </tr>
      </xsl:if>
      <xsl:if test="boolean(string-length(//system))">
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
      </xsl:if>
      <xsl:if test="boolean(string-length(//access))">
        <tr>
          <td bgcolor="#aaddaa">アクセス先</td>
          <td>
            <xsl:if test="boolean(string-length(//access))">
              <a href="{//access}"><xsl:value-of select="//access"/></a>
            </xsl:if>
          </td>
        </tr>
      </xsl:if>
      <xsl:if test="boolean(string-length(//condition))">
        <tr>
          <td bgcolor="#aaddaa">利用条件</td>
          <td><xsl:value-of select="//condition"/></td>
        </tr>
      </xsl:if>
      <xsl:if test="boolean(string-length(//format))">
        <tr>
          <td bgcolor="#aaddaa">データ提供形態</td>
          <td><xsl:value-of select="//format"/></td>
        </tr>
      </xsl:if>
      <xsl:if test="boolean(string-length(//contributor))">
        <xsl:apply-templates select="//contributor" />
      </xsl:if>
      <tr>
        <td bgcolor="#aaddaa">登録者</td>
        <td>
          <a href="personal.cgi?userid={//userid}"><xsl:value-of select="//userid"/></a>
        </td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">作成日</td>
        <td>
          <xsl:value-of select="//created_date"/>
        </td>
      </tr>
      <tr>
        <td bgcolor="#aaddaa">更新日</td>
        <td>
          <xsl:value-of select="//update_date"/>
        </td>
      </tr>
    </table>
    <xsl:if test="boolean(string-length(//source_id))">
      <p>
        この情報は<a href="browse.cgi?id={//source_id}"><xsl:value-of select="//source_id"/></a>を元に作成しています。
    </p>
  </xsl:if>  
    </xsl:template>
  <xsl:template match="//contributor">
      <tr>
        <td bgcolor="#aaddaa">コントリビュータ</td>
        <td><a href="browse.cgi?scan=contributor;search={.}"><xsl:value-of select="."/></a></td>
      </tr>
    
  </xsl:template>
  <xsl:template match="//subject">
      <tr>
        <td bgcolor="#aaddaa">主題</td>
        <td><a href="browse.cgi?scan=subject;search={.}"><xsl:value-of select="."/></a></td>
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
