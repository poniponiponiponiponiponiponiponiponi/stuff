use crate::context::Context;

pub fn error(ctx: &mut Context, line: usize, msg: &str) {
    report(ctx, line, "", msg);
}

fn report(ctx: &mut Context, line: usize, where_: &str, msg: &str) {
    eprintln!("[line {line}] Error {where_}: {msg}");
    ctx.had_error = true;
}
