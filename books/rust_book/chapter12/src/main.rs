use std::env;
use std::process;
use chapter12::Config;

fn main() {
    let args: Vec<String> = env::args().collect();

    let config = Config::build(&args).unwrap_or_else(|err| {
        println!("problem parsing args: {}", err);
        process::exit(1);
    });

    println!("searching for {}", config.query);
    println!("in file {}", config.file_path);

    if let Err(e) = chapter12::run(config) {
        eprintln!("Program error: {}", e);
        process::exit(2);
    }
}

