use std::fs;
use std::collections::HashMap;

fn parse() -> Vec<String> {
    fs::read_to_string("input").unwrap().lines().map(String::from).collect()
}

fn main() {
    let mut board = parse();
    let mut board2 = parse();
    let mut antidotes = HashMap::<u8, Vec<(isize, isize)>>::new();
    let mut ans = 0;
    for y1 in 0..board.len() {
        for x1 in 0..board[y1].len() {
            let c1 = board[y1].as_bytes()[x1];
            if c1 == b'.' {
                continue;
            }
            for y2 in 0..board.len() {
                for x2 in 0..board[y2].len() {
                    if x1 == x2 && y1 == y2 {
                        continue;
                    }
                    let c2 = board[y2].as_bytes()[x2];
                    if c1 != c2 {
                        continue;
                    }
                    
                    let x_diff = x2 as isize - x1 as isize;
                    let y_diff = y2 as isize - y1 as isize;
                    let mut new_x = x2 as isize;
                    let mut new_y = y2 as isize;
                    loop {
                        new_x += x_diff;
                        new_y += y_diff;
                        if new_x < 0 || new_x >= board[0].len() as isize ||
                            new_y < 0 || new_y >= board.len() as isize {
                                break;
                            }
                        if antidotes.entry(b'a').or_insert_with(Vec::new).iter().find(|p| **p == (new_x, new_y)).is_some() {
                            continue;
                        }
                        antidotes.entry(b'a').or_insert_with(Vec::new).push((new_x, new_y));
                        ans += 1;
                        board2[new_y as usize]
                            .replace_range(new_x as usize..new_x as usize + 1, "#");                        
                    }
                }
            }
        }
    }

    // hacky!
    for l in &board2 {
        for c in l.chars() {
            if c != '.' && c != '#' {
                ans += 1;
            }
        }
    }

    println!("{}", ans);
    for l in board2 {
        println!("{}", l);
    }
}
