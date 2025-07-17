pub struct Context {
    pub had_error: bool,
}

impl Context {
    pub fn new() -> Context {
        Context {
            had_error: false
        }
    }
}
