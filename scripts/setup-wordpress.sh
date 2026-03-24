#!/bin/bash
set -e

echo ">>> Waiting for WordPress to be ready..."
until curl -s http://wordpress:80 > /dev/null; do
  sleep 3
done

echo ">>> Installing WordPress core..."
wp core install \
  --path=/var/www/html \
  --url="http://localhost:8080" \
  --title="QA Automation Store" \
  --admin_user="admin" \
  --admin_password="admin_password" \
  --admin_email="qa@test.com" \
  --skip-email \
  --allow-root

echo ">>> Installing WooCommerce plugin..."
wp plugin install woocommerce \
  --path=/var/www/html \
  --activate \
  --allow-root

echo ">>> Installing Basic Auth plugin..."
wp plugin install https://github.com/WP-API/Basic-Auth/archive/master.zip \
  --activate \
  --force \
  --path=/var/www/html \
  --allow-root || true

echo ">>> Running WooCommerce setup..."
wp wc --user=admin tool run install_pages \
  --path=/var/www/html \
  --allow-root

echo ">>> Setting permalink structure..."
wp rewrite structure "/%postname%/" \
  --path=/var/www/html \
  --allow-root
wp rewrite flush \
  --path=/var/www/html \
  --allow-root

echo ">>> Disabling SSL requirements..."
wp eval '
update_option("woocommerce_force_ssl_checkout", "no");
update_option("woocommerce_api_enabled", "yes");
' --path=/var/www/html --allow-root

echo ">>> Generating WooCommerce REST API key..."
wp eval '
$user_id = 1;
$consumer_key    = "ck_" . wc_rand_hash();
$consumer_secret = "cs_" . wc_rand_hash();
global $wpdb;
$wpdb->insert(
    $wpdb->prefix . "woocommerce_api_keys",
    array(
        "user_id"         => $user_id,
        "description"     => "qa-automation",
        "permissions"     => "read_write",
        "consumer_key"    => wc_api_hash( $consumer_key ),
        "consumer_secret" => $consumer_secret,
        "truncated_key"   => substr( $consumer_key, -7 ),
        "last_access"     => null,
    ),
    array( "%d", "%s", "%s", "%s", "%s", "%s", "%s" )
);
if ( $wpdb->last_error ) {
    echo "DB_ERROR: " . $wpdb->last_error . "\n";
} else {
    echo "CONSUMER_KEY=" . $consumer_key . "\n";
    echo "CONSUMER_SECRET=" . $consumer_secret . "\n";
}
' --path=/var/www/html --allow-root > /tmp/api_output.txt

cat /tmp/api_output.txt

if grep -q "DB_ERROR" /tmp/api_output.txt; then
  echo "Failed to insert API key"
  exit 1
fi

CONSUMER_KEY=$(grep "CONSUMER_KEY=" /tmp/api_output.txt | cut -d'=' -f2)
CONSUMER_SECRET=$(grep "CONSUMER_SECRET=" /tmp/api_output.txt | cut -d'=' -f2)

echo "BASE_URL=http://wordpress/wp-json/wc/v3" > /shared/.env
echo "CONSUMER_KEY=admin" >> /shared/.env
echo "CONSUMER_SECRET=admin_password" >> /shared/.env

touch /shared/ready
echo ">>> Setup complete!"