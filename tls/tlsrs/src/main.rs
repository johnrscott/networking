use rustls::{Writer, Connection};
use std::io;
use std::sync::Arc;
use std::io::Write;

fn main() {
    let mut root_store = rustls::RootCertStore::empty();
    root_store.add_server_trust_anchors(webpki_roots::TLS_SERVER_ROOTS.0.iter().map(|ta| {
        rustls::OwnedTrustAnchor::from_subject_spki_name_constraints(
            ta.subject,
            ta.spki,
            ta.name_constraints,
        )
    }));

    let config = rustls::ClientConfig::builder()
        .with_safe_defaults()
        .with_root_certificates(root_store)
        .with_no_client_auth();

    let rc_config = Arc::new(config);
    let example_com = "devbert".try_into().unwrap();
    let mut client = rustls::ClientConnection::new(rc_config, example_com)
        .unwrap();

    client.writer().write(b"GET / HTTP/1.0\r\n\r\n").unwrap();
}
