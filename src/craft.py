#!/usr/bin/env python
# -*- coding: utf-8 -*-

from newsapi.articles import Articles
import requests
import os

from urlparse import urlparse

import datetime

import jinja2

def craft_newsletter():
    '''
    Craft the newsletter. Returns JSON.
    :return: the newsletter json
    '''

    a = Articles(API_KEY=os.environ["NEWSAPI_KEY"])
    top_results = a.get_by_top(source="google-news")

    breaking = requests.get("https://librenews.io/api").json()["latest"]

    period = "AM"
    greeting = "It's 5:30 ZULU time."

    if datetime.datetime.now(tz=None).time() > datetime.time(12):
        period = "PM"
        greeting = "It's 17:30 ZULU time."

    name = period + " - " + datetime.date.today().strftime("%A, %d %B %Y")

    for story in top_results["articles"]:
        story["source"] = urlparse(story["url"]).netloc

    return {
        "top_stories": top_results["articles"][:3],
        "breaking": [story for story in breaking if story["channel"] == "Breaking News"][:5],
        "name": name,
        "greeting": greeting
    }

def craft_html(newsletter):
    base_template = '''
    <!doctype html>
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">

    <head>
    	<!--[if gte mso 15]>
    		<xml>
    			<o:OfficeDocumentSettings>
    			<o:AllowPNG/>
    			<o:PixelsPerInch>96</o:PixelsPerInch>
    			</o:OfficeDocumentSettings>
    		</xml>
    		<![endif]-->
    	<meta charset="UTF-8">
    	<meta http-equiv="X-UA-Compatible" content="IE=3Dedge">
    	<meta name="viewport" content="width=3Ddevice-width, initial-scale=3D1">
    	<title>{{name}}</title>

    	<style type="text/css">
    		p {
    			margin: 10px 0;
    			padding: 0;
    		}

    		table {
    			border-collapse: collapse;
    		}

    		h1,
    		h2,
    		h3,
    		h4,
    		h5,
    		h6 {
    			display: block;
    			margin: 0;
    			padding: 0;
    		}

    		img,
    		a img {
    			border: 0;
    			height: auto;
    			outline: none;
    			text-decoration: none;
    		}

    		body,
    		#bodyTable,
    		#bodyCell {
    			height: 100%;
    			margin: 0;
    			padding: 0;
    			width: 100%;
    		}

    		.mcnPreviewText {
    			display: none !important;
    		}

    		#outlook a {
    			padding: 0;
    		}

    		img {
    			-ms-interpolation-mode: bicubic;
    		}

    		table {
    			mso-table-lspace: 0pt;
    			mso-table-rspace: 0pt;
    		}

    		.ReadMsgBody {
    			width: 100%;
    		}

    		.ExternalClass {
    			width: 100%;
    		}

    		p,
    		a,
    		li,
    		td,
    		blockquote {
    			mso-line-height-rule: exactly;
    		}

    		a[href^=3Dtel],
    		a[href^=3Dsms] {
    			color: inherit;
    			cursor: default;
    			text-decoration: none;
    		}

    		p,
    		a,
    		li,
    		td,
    		body,
    		table,
    		blockquote {
    			-ms-text-size-adjust: 100%;
    			-webkit-text-size-adjust: 100%;
    		}

    		.ExternalClass,
    		.ExternalClass p,
    		.ExternalClass td,
    		.ExternalClass div,
    		.ExternalClass span,
    		.ExternalClass font {
    			line-height: 100%;
    		}

    		a[x-apple-data-detectors] {
    			color: inherit !important;
    			text-decoration: none !important;
    			font-size: inherit !important;
    			font-family: inherit !important;
    			font-weight: inherit !important;
    			line-height: inherit !important;
    		}

    		.templateContainer {
    			max-width: 600px !important;
    		}

    		a.mcnButton {
    			display: block;
    		}

    		.mcnImage,
    		.mcnRetinaImage {
    			vertical-align: bottom;
    		}

    		.mcnTextContent {
    			word-break: break-word;
    		}

    		.mcnTextContent img {
    			height: auto !important;
    		}

    		.mcnDividerBlock {
    			table-layout: fixed !important;
    		}

    		h1 {
    			color: #222222;
    			font-family: Helvetica;
    			font-size: 40px;
    			font-style: normal;
    			font-weight: bold;
    			line-height: 150%;
    			letter-spacing: normal;
    			text-align: center;
    		}

    		h2 {
    			color: #222222;
    			font-family: Helvetica;
    			font-size: 34px;
    			font-style: normal;
    			font-weight: bold;
    			line-height: 150%;
    			letter-spacing: normal;
    			text-align: left;
    		}

    		h3 {
    			color: #444444;
    			font-family: Helvetica;
    			font-size: 22px;
    			font-style: normal;
    			font-weight: bold;
    			line-height: 150%;
    			letter-spacing: normal;
    			text-align: left;
    		}

    		h4 {
    			color: #999999;
    			font-family: Georgia;
    			font-size: 20px;
    			font-style: italic;
    			font-weight: normal;
    			line-height: 125%;
    			letter-spacing: normal;
    			text-align: left;
    		}

    		#templateHeader {
    			background-color: #1024db;
    			background-image: none;
    			background-repeat: no-repeat;
    			background-position: center;
    			background-size: cover;
    			border-top: 0;
    			border-bottom: 0;
    			padding-top: 28px;
    			padding-bottom: 28px;
    		}

    		.headerContainer {
    			background-color: transparent;
    			background-image: none;
    			background-repeat: no-repeat;
    			background-position: center;
    			background-size: cover;
    			border-top: 0;
    			border-bottom: 0;
    			padding-top: 0;
    			padding-bottom: 0;
    		}

    		.headerContainer .mcnTextContent,
    		.headerContainer .mcnTextContent p {
    			color: #808080;
    			font-family: Helvetica;
    			font-size: 16px;
    			line-height: 150%;
    			text-align: left;
    		}

    		.headerContainer .mcnTextContent a,
    		.headerContainer .mcnTextContent p a {
    			color: #00ADD8;
    			font-weight: normal;
    			text-decoration: underline;
    		}

    		#templateBody {
    			background-color: #ffffff;
    			background-image: none;
    			background-repeat: no-repeat;
    			background-position: center;
    			background-size: cover;
    			border-top: 0;
    			border-bottom: 0;
    			padding-top: 27px;
    			padding-bottom: 54px;
    		}

    		.bodyContainer {
    			background-color: #transparent;
    			background-image: none;
    			background-repeat: no-repeat;
    			background-position: center;
    			background-size: cover;
    			border-top: 0;
    			border-bottom: 0;
    			padding-top: 0;
    			padding-bottom: 0;
    		}

    		.bodyContainer .mcnTextContent,
    		.bodyContainer .mcnTextContent p {
    			color: #808080;
    			font-family: Helvetica;
    			font-size: 16px;
    			line-height: 150%;
    			text-align: left;
    		}

    		.bodyContainer .mcnTextContent a,
    		.bodyContainer .mcnTextContent p a {
    			color: #1024db;
    			font-weight: normal;
    			text-decoration: underline;
    		}

    		#templateFooter {
    			background-color: #333333;
    			background-image: none;
    			background-repeat: no-repeat;
    			background-position: center;
    			background-size: cover;
    			border-top: 0;
    			border-bottom: 0;
    			padding-top: 45px;
    			padding-bottom: 63px;
    		}

    		.footerContainer {
    			background-color: transparent;
    			background-image: none;
    			background-repeat: no-repeat;
    			background-position: center;
    			background-size: cover;
    			border-top: 0;
    			border-bottom: 0;
    			padding-top: 0;
    			padding-bottom: 0;
    		}

    		.footerContainer .mcnTextContent,
    		.footerContainer .mcnTextContent p {
    			color: #FFFFFF;
    			font-family: Helvetica;
    			font-size: 12px;
    			line-height: 150%;
    			text-align: center;
    		}

    		.footerContainer .mcnTextContent a,
    		.footerContainer .mcnTextContent p a {
    			color: #FFFFFF;
    			font-weight: normal;
    			text-decoration: underline;
    		}

    		@media only screen and (min-width:768px) {
    			.templateContainer {
    				width: 600px !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			body,
    			table,
    			td,
    			p,
    			a,
    			li,
    			blockquote {
    				-webkit-text-size-adjust: none !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			body {
    				width: 100% !important;
    				min-width: 100% !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.mcnRetinaImage {
    				max-width: 100% !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.mcnImage {
    				width: 100% !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.mcnCartContainer,
    			.mcnCaptionTopContent,
    			.mcnRecContentContainer,
    			.mcnCaptionBottomContent,
    			.mcnTextContentContainer,
    			.mcnBoxedTextContentContainer,
    			.mcnImageGroupContentContainer,
    			.mcnCaptionLeftTextContentContainer,
    			.mcnCaptionRightTextContentContainer,
    			.mcnCaptionLeftImageContentContainer,
    			.mcnCaptionRightImageContentContainer,
    			.mcnImageCardLeftTextContentContainer,
    			.mcnImageCardRightTextContentContainer,
    			.mcnImageCardLeftImageContentContainer,
    			.mcnImageCardRightImageContentContainer {
    				max-width: 100% !important;
    				width: 100% !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.mcnBoxedTextContentContainer {
    				min-width: 100% !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.mcnImageGroupContent {
    				padding: 9px !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.mcnCaptionLeftContentOuter .mcnTextContent,
    			.mcnCaptionRightContentOuter .mcnTextContent {
    				padding-top: 9px !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.mcnImageCardTopImageContent,
    			.mcnCaptionBottomContent:last-child .mcnCaptionBottomImageContent,
    			.mcnCaptionBlockInner .mcnCaptionTopContent:last-child .mcnTextContent {
    				padding-top: 18px !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.mcnImageCardBottomImageContent {
    				padding-bottom: 9px !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.mcnImageGroupBlockInner {
    				padding-top: 0 !important;
    				padding-bottom: 0 !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.mcnImageGroupBlockOuter {
    				padding-top: 9px !important;
    				padding-bottom: 9px !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.mcnTextContent,
    			.mcnBoxedTextContentColumn {
    				padding-right: 18px !important;
    				padding-left: 18px !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.mcnImageCardLeftImageContent,
    			.mcnImageCardRightImageContent {
    				padding-right: 18px !important;
    				padding-bottom: 0 !important;
    				padding-left: 18px !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.mcpreview-image-uploader {
    				display: none !important;
    				width: 100% !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			h1 {
    				font-size: 30px !important;
    				line-height: 125% !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			h2 {
    				font-size: 26px !important;
    				line-height: 125% !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			h3 {
    				font-size: 20px !important;
    				line-height: 150% !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			h4 {
    				font-size: 18px !important;
    				line-height: 150% !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.mcnBoxedTextContentContainer .mcnTextContent,
    			.mcnBoxedTextContentContainer .mcnTextContent p {
    				font-size: 14px !important;
    				line-height: 150% !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.headerContainer .mcnTextContent,
    			.headerContainer .mcnTextContent p {
    				font-size: 16px !important;
    				line-height: 150% !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.bodyContainer .mcnTextContent,
    			.bodyContainer .mcnTextContent p {
    				font-size: 16px !important;
    				line-height: 150% !important;
    			}

    		}

    		@media only screen and (max-width: 480px) {
    			.footerContainer .mcnTextContent,
    			.footerContainer .mcnTextContent p {
    				font-size: 14px !important;
    				line-height: 150% !important;
    			}

    		}
    	</style>
    </head>

    <body style="height: 100%;margin: 0;padding: 0;width: 100%;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    	<!--
    -->
    	<center>
    		<table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;height: 100%;margin: 0;padding: 0;width: 100%;">
    			<tr>
    				<td align="center" valign="top" id="bodyCell" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;height: 100%;margin: 0;padding: 0;width: 100%;">
    					<!-- BEGIN TEMPLATE // -->
    					<table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    						<tr>
    							<td align="center" valign="top" id="templateHeader" data-template-container="" style="background:#1024db none no-repeat center/cover;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #1024db;background-image: none;background-repeat: no-repeat;background-position: center;background-size: cover;border-top: 0;border-bottom: 0;padding-top: 28px;padding-bottom: 28px;">
    								<!--[if (gte mso 9)|(IE)]>
    									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
    									<tr>
    									<td align="center" valign="top" width="600" style="width:600px;">
    									<![endif]-->
    								<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
    									<tr>
    										<td valign="top" class="headerContainer" style="background:transparent none no-repeat center/cover;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: transparent;background-image: none;background-repeat: no-repeat;background-position: center;background-size: cover;border-top: 0;border-bottom: 0;padding-top: 0;padding-bottom: 0;">
    											<table class="mcnTextBlock" style="min-width: 100%;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" width="100%" cellspacing="0" cellpadding="0" border="0">
    												<tbody class="mcnTextBlockOuter">
    													<tr>
    														<td class="mcnTextBlockInner" style="padding-top: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" valign="top">
    															<!--[if mso]>
    				<table align="left" border="0" cellspacing="0" cellpadding="0" width="100%" style="width:100%;">
    				<tr>
    				<![endif]-->

    															<!--[if mso]>
    				<td valign="top" width="600" style="width:600px;">
    				<![endif]-->
    															<table style="max-width: 100%;min-width: 100%;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnTextContentContainer" width="100%" cellspacing="0" cellpadding="0"
    															  border="0" align="left">
    																<tbody>
    																	<tr>

    																		<td class="mcnTextContent" style="padding-top: 0;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #808080;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;"
    																		  valign="top">

    																			<h1 class="null" style="text-align: center;display: block;margin: 0;padding: 0;color: #222222;font-family: Helvetica;font-size: 40px;font-style: normal;font-weight: bold;line-height: 150%;letter-spacing: normal;"><span style="color:#FFFFFF"><span style="font-size:64px"><span style="font-family:helvetica neue,helvetica,arial,verdana,sans-serif"><strong>530ZULU</strong></span></span></span></h1>

    																			<h3 class="null" style="text-align: center;display: block;margin: 0;padding: 0;color: #444444;font-family: Helvetica;font-size: 22px;font-style: normal;font-weight: bold;line-height: 150%;letter-spacing: normal;"><span style="color:#FFFFFF"><span style="font-size:24px"><span style="font-family:helvetica neue,helvetica,arial,verdana,sans-serif">PM - Sunday, 15 April 2018</span></span></span></h3>

    																		</td>
    																	</tr>
    																</tbody>
    															</table>
    															<!--[if mso]>
    				</td>
    				<![endif]-->

    															<!--[if mso]>
    				</tr>
    				</table>
    				<![endif]-->
    														</td>
    													</tr>
    												</tbody>
    											</table>
    										</td>
    									</tr>
    								</table>
    								<!--[if (gte mso 9)|(IE)]>
    									</td>
    									</tr>
    									</table>
    									<![endif]-->
    							</td>
    						</tr>
    						<tr>
    							<td align="center" valign="top" id="templateBody" data-template-container="" style="background:#ffffff none no-repeat center/cover;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #ffffff;background-image: none;background-repeat: no-repeat;background-position: center;background-size: cover;border-top: 0;border-bottom: 0;padding-top: 27px;padding-bottom: 54px;">
    								<!--[if (gte mso 9)|(IE)]>
    									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
    									<tr>
    									<td align="center" valign="top" width="600" style="width:600px;">
    									<![endif]-->
    								<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
    									<tr>
    										<td valign="top" class="bodyContainer" style="background:#transparent none no-repeat center/cover;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #transparent;background-image: none;background-repeat: no-repeat;background-position: center;background-size: cover;border-top: 0;border-bottom: 0;padding-top: 0;padding-bottom: 0;">
    											<table class="mcnTextBlock" style="min-width: 100%;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" width="100%" cellspacing="0" cellpadding="0" border="0">
    												<tbody class="mcnTextBlockOuter">
    													<tr>
    														<td class="mcnTextBlockInner" style="padding-top: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" valign="top">
    															<!--[if mso]>
    				<table align="left" border="0" cellspacing="0" cellpadding="0" width="100%" style="width:100%;">
    				<tr>
    				<![endif]-->
    															<!--[if mso]>
    				<td valign="top" width="600" style="width:600px;">
    				<![endif]-->
    															<table style="max-width: 100%;min-width: 100%;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnTextContentContainer" width="100%" cellspacing="0" cellpadding="0"
    															  border="0" align="left">
    																<tbody>
    																	<tr>

    																		<td class="mcnTextContent" style="padding-top: 0;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #808080;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;"
    																		  valign="top">

    																			<h1 style="display: block;margin: 0;padding: 0;color: #222222;font-family: Helvetica;font-size: 40px;font-style: normal;font-weight: bold;line-height: 150%;letter-spacing: normal;text-align: center;">Here's the latest...</h1>

    																		</td>
    																	</tr>
    																</tbody>
    															</table>
    															<!--[if mso]>
    				</td>
    				<![endif]-->

    															<!--[if mso]>
    				</tr>
    				</table>
    				<![endif]-->
    														</td>
    													</tr>
    												</tbody>
    											</table>
    											<table class="mcnDividerBlock" style="min-width: 100%;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;table-layout: fixed !important;" width="100%" cellspacing="0" cellpadding="0"
    											  border="0">
    												<tbody class="mcnDividerBlockOuter">
    													<tr>
    														<td class="mcnDividerBlockInner" style="min-width: 100%;padding: 18px 18px 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    															<table class="mcnDividerContent" style="min-width: 100%;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" width="100%" cellspacing="0" cellpadding="0" border="0">
    																<tbody>
    																	<tr>
    																		<td style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    																			<span></span>
    																		</td>
    																	</tr>
    																</tbody>
    															</table>
    															<!--
                    <td class="mcnDividerBlockInner" style="padding: 18px;">
                    <hr class="mcnDividerContent" style="border-bottom-color:none; border-left-color:none; border-right-color:none; border-bottom-width:0; border-left-width:0; border-right-width:0; margin-top:0; margin-right:0; margin-bottom:0; margin-left:0;" />
    -->
    														</td>
    													</tr>
    												</tbody>
    											</table>
    											{% for story in stories %}
    											<table class="mcnTextBlock" style="min-width: 100%;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" width="100%" cellspacing="0" cellpadding="0" border="0">
    												<tbody class="mcnTextBlockOuter">
    													<tr>
    														<td class="mcnTextBlockInner" style="padding-top: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" valign="top">
    															<!--[if mso]>
    				<table align="left" border="0" cellspacing="0" cellpadding="0" width="100%" style="width:100%;">
    				<tr>
    				<![endif]-->
    															<!--[if mso]>
    				<td valign="top" width="600" style="width:600px;">
    				<![endif]-->
    															<table style="max-width: 100%;min-width: 100%;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnTextContentContainer" width="100%" cellspacing="0" cellpadding="0"
    															  border="0" align="left">
    																<tbody>
    																	<tr>

    																		<td class="mcnTextContent" style="padding-top: 0;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #808080;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;"
    																		  valign="top">

    																			<h4 style="display: block;margin: 0;padding: 0;color: #999999;font-family: Georgia;font-size: 20px;font-style: italic;font-weight: normal;line-height: 125%;letter-spacing: normal;text-align: left;"><span style="color:#696969"><strong><span style="font-family:helvetica neue,helvetica,arial,verdana,sans-serif">{{story.title}}</span></strong></span></h4>

    																		</td>
    																	</tr>
    																</tbody>
    															</table>
    															<!--[if mso]>
    				</td>
    				<![endif]-->

    															<!--[if mso]>
    				</tr>
    				</table>
    				<![endif]-->
    														</td>
    													</tr>
    												</tbody>
    											</table>
    											<table class="mcnTextBlock" style="min-width: 100%;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" width="100%" cellspacing="0" cellpadding="0" border="0">
    												<tbody class="mcnTextBlockOuter">
    													<tr>
    														<td class="mcnTextBlockInner" style="padding-top: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" valign="top">
    															<!--[if mso]>
    				<table align="left" border="0" cellspacing="0" cellpadding="0" width="100%" style="width:100%;">
    				<tr>
    				<![endif]-->
    															<!--[if mso]>
    				<td valign="top" width="600" style="width:600px;">
    				<![endif]-->
    															<table style="max-width: 100%;min-width: 100%;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnTextContentContainer" width="100%" cellspacing="0" cellpadding="0"
    															  border="0" align="left">
    																<tbody>
    																	<tr>

    																		<td class="mcnTextContent" style="padding-top: 0;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #808080;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;"
    																		  valign="top">

    																			{{story.description}} <a href="{{story.url}}" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: black;font-weight: normal;text-decoration: underline;">{{story.source}}.</a>
    																		</td>
    																	</tr>
    																</tbody>
    															</table>
    															<!--[if mso]>
    				</td>
    				<![endif]-->

    															<!--[if mso]>
    				</tr>
    				</table>
    				<![endif]-->
    														</td>
    													</tr>
    												</tbody>
    											</table>
                                                <br \>
    											{% endfor %}
    										</td>
    									</tr>
    								</table>
    								<!--[if (gte mso 9)|(IE)]>
    									</td>
    									</tr>
    									</table>
    									<![endif]-->
    							</td>
    						</tr>
    					</table>
    				</td>
    			</tr>
    		</table>
    	</center>
    </body>

    </html>
    '''
    template = jinja2.Template(base_template)
    html = template.render(name=newsletter["name"], stories=newsletter["top_stories"], breaking=newsletter["breaking"], greeting=newsletter["greeting"])
    return html

def craft_text(newsletter):
    base_template = '''{{name}} (TEXT ONLY VERSION)

Top Stories
------------------

{% for story in stories %}
{{story.title}}
{{story.description}}
{{story.url}}
{% endfor %}

-----
Powered by LibreNews, NewsAPI, and Google News. Created by Miles McCain.'''
    template = jinja2.Template(base_template)
    text = template.render(name=newsletter["name"], stories=newsletter["top_stories"], breaking=newsletter["breaking"], greeting=newsletter["greeting"])
    return text
