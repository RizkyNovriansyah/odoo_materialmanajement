# odoo_materialmanajement
odoo_materialmanajement

chmod -R 755 ~/odoo14/addons/odoo_materialmanagement
chown -R $(whoami) ~/odoo14/addons/odoo_materialmanagement

--
untuk run
python odoo-bin -c ~/odoo14/odoo.conf -u odoo_materialmanajement --log-level=debug

untuk unit testing
python odoo-bin --test-enable --log-level=test --stop-after-init -d odoo_tes -i odoo_materialmanajement

unarchive setelah menambahkan accessright