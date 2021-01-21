# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "POS Order On Website",
  "summary"              :  """The customers can now track their POS orders from their Odoo website customer account. The module shows the list of all the POS orders from the customer.""",
  "category"             :  "Point of Sale",
  "version"              :  "1.1.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "maintainer"           :  "Saurabh Gupta",
  "website"              :  "https://store.webkul.com/Odoo-POS-Order-On-Website.html",
  "description"          :  """Odoo POS Order On Website
POS view orders on website
View POS order on website account
Track POS order in account
POS order in website account""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_website",
  "depends"              :  [
                             'point_of_sale',
                             'portal',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/website_portal_inherit_template.xml',
                            ],
  "demo"                 :  ['data/pos_website_demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  30,
  "currency"             :  "USD",
}