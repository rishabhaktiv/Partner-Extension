import base64
from odoo import models, fields, tools, SUPERUSER_ID, _, Command, api

class ResPartnerInherited(models.Model):
    _inherit = "res.partner"

    secondary_email = fields.Char(string="Secondary Email")
    social_facebook = fields.Char(string="Social Facebook")
    social_twitter = fields.Char(string="Social Twitter")
    social_linkedin = fields.Char(string="Social LinkedIn")
    date_first_contact = fields.Date(string="Date First Contact")
    loyalty_points = fields.Integer(string="Loyalty Points")
    preferred_language = fields.Selection(
        [('en', 'English'), ('es', 'Spanish'), ('fr', 'French')],
        string="Preferred Language", default="en")
    is_vip = fields.Boolean(string="Is VIP", default=False)
    birthday_reminder = fields.Date(string="Birthday Reminder", default=False)
    region = fields.Many2one('res.region', string="Region")
    partner_rating = fields.Integer(string="Partner Rating")


class ResPartnerExtended(models.Model):
    _name = "res.partner.extended"
    _inherit = "res.partner"

    active = fields.Boolean(default=True)
    channel_ids = fields.Many2many(
        "discuss.channel",
        "discuss_channel_member_extended",  # Intermediary table name
        "res_partner_extended_id",          # FK to res.partner.extended
        "extended_channel_id",              # FK to discuss.channel
        string="Extended Channels",
        copy=False,
        ondelete="cascade"
    )
    starred_message_ids = fields.Many2many('mail.message',
                                           'mail_message_res_partner_starred_extended_rel')
    commercial_partner_id = fields.Many2one(
        'res.partner', string='Commercial Entity',
        compute='_compute_commercial_partner', store=True,
        recursive=True, index=True)

    def _compute_avatar(self, avatar_field, image_field):
        partners_with_internal_user = self.filtered(lambda partner: partner.user_ids - partner.user_ids.filtered('share'))
        super(ResPartnerExtended, partners_with_internal_user)._compute_avatar(avatar_field, image_field)
        partners_without_image = (self - partners_with_internal_user).filtered(lambda p: not p[image_field])
        for _, group in tools.groupby(partners_without_image, key=lambda p: p._avatar_get_placeholder_path()):
            group_partners = self.env['res.partner.extended'].concat(*group)
            group_partners[avatar_field] = base64.b64encode(group_partners[0]._avatar_get_placeholder())

        for partner in self - partners_with_internal_user - partners_without_image:
            partner[avatar_field] = partner[image_field]

    @api.depends('is_company', 'parent_id.commercial_partner_id')
    def _compute_commercial_partner(self):
        pass
        import pdb;
        pdb.set_trace()
        for partner in self:
            if partner.is_company or not partner.parent_id:
                partner.commercial_partner_id = partner.id if partner._origin else False
            else:
                partner.commercial_partner_id = partner.parent_id.commercial_partner_id.id if partner._origin else False

    @api.depends('user_ids.share', 'user_ids.active')
    def _compute_partner_share(self):
        import pdb;
        pdb.set_trace()
        super_partner = self.env['res.users'].browse(SUPERUSER_ID).partner_id
        if super_partner in self:
            super_partner.partner_share = False
        for partner in self - super_partner:
            partner.partner_share = not partner.user_ids or not any(
                not user.share for user in partner.user_ids)

    # def init(self):
    #     # Check if the column does not already exist
    #     if not sql.column_exists(self.env.cr, "res_partner_extended",
    #                              "signup_token"):
    #         self.env.cr.execute("""
    #             ALTER TABLE res_partner_extended ADD COLUMN signup_token varchar
    #         """)

