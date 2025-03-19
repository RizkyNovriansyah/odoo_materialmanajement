# odoo_materialmanajement
odoo_materialmanajement

Dokumentasi Pengembangan
https://docs.google.com/document/d/1tjfOiZzuekkCo2oWyAm6zYfN7yJ_tKHMQCtbgKMRv6k/edit?tab=t.0 

chmod -R 755 ~/odoo14/addons/odoo_materialmanagement
chown -R $(whoami) ~/odoo14/addons/odoo_materialmanagement

--
untuk run
python odoo-bin -c ~/odoo14/odoo.conf -u odoo_materialmanajement --log-level=debug

untuk unit testing
python odoo-bin --test-enable --log-level=test --stop-after-init -d odoo_tes -i odoo_materialmanajement
python -m unittest ~/odoo14/odoo/addons/odoo_materialmanajement/unit_test.py -v

unarchive setelah menambahkan accessright