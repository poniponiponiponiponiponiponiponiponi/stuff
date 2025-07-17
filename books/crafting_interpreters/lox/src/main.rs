use std::env;
use std::error::Error;
use std::fs;
use std::io;
use lox::scanner::Scanner;
use lox::context::Context;

fn run(ctx: &mut Context, source: &str) {
    let mut scanner = Scanner::from(source);
    let tokens = scanner.scan_tokens(ctx);
    for token in tokens {
        dbg!(token);
    }
}

fn run_file(ctx: &mut Context, file: &str) -> io::Result<()> {
    let content = fs::read_to_string(file)?;
    run(ctx, &content);
    Ok(())
}

fn run_prompt(ctx: &mut Context) {
    let mut line = String::new();
    let stdin = io::stdin();
    loop {
        print!("> ");
        stdin.read_line(&mut line).unwrap();
        let line = line.trim();
        if line == "" {
            break;
        }
        run(ctx, line);
    }
    
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = env::args().collect::<Vec<String>>();
    let mut ctx = Context::new();
    if args.len() > 2 {
        println!("Usage: {} [script]", args[0]);
    } else if args.len() == 2 {
        run_file(&mut ctx, &args[1])?;
    } else {
        run_prompt(&mut ctx);
    }

    Ok(())
}
