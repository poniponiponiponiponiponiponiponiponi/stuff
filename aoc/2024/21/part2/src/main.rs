use std::fs;

fn num_kb(from: char) -> (i32, i32) {
    match from {
        '7' => (0, 0),
        '8' => (1, 0),
        '9' => (2, 0),
        '4' => (0, 1),
        '5' => (1, 1),
        '6' => (2, 1),
        '1' => (0, 2),
        '2' => (1, 2),
        '3' => (2, 2),
        
        '0' => (1, 3),
        'A' => (2, 3),
        _ => panic!("asd"),
    }
}

fn dir_kb(from: char) -> (i32, i32) {
    match from {
        
        'w' => (1, 0),
        'A' => (2, 0),
        'a' => (0, 1),
        's' => (1, 1),
        'd' => (2, 1),
        _ => panic!("dsa"),
    }
}

fn get_cands(is_num_kb: bool, from_b: char, to_b: char) -> Vec<String> {
    let from_coord = if is_num_kb {
        num_kb(from_b)
    } else {
        dir_kb(from_b)
    };
    let to_coord = if is_num_kb {
        num_kb(to_b)
    } else {
        dir_kb(to_b)
    };

    let diff = (to_coord.0 - from_coord.0, to_coord.1 - from_coord.1);
    let vertical = if diff.1 >= 0 {
        "s".repeat(diff.1.abs() as usize)
    } else {
        "w".repeat(diff.1.abs() as usize)
    };
    let horizontal = if diff.0 >= 0 {
        "d".repeat(diff.0.abs() as usize)
    } else {
        "a".repeat(diff.0.abs() as usize)
    };
    let mut cands = Vec::new();

    if is_num_kb {
        if !(from_coord.1 == 3 && to_coord.0 == 0) {
            cands.push(format!("{}{}{}", &horizontal, &vertical, 'A').to_string());
        }
        if !(from_coord.0 == 0 && to_coord.1 == 3) {
            cands.push(format!("{}{}{}", &vertical, &horizontal, 'A').to_string());
        }
    } else {
        if !(from_coord.0 == 0 && to_coord.1 == 0) {
            cands.push(format!("{}{}{}", &vertical, &horizontal, 'A').to_string());
        }
        if !(from_coord.1 == 0 && to_coord.0 == 0) {
            cands.push(format!("{}{}{}", &horizontal, &vertical, 'A').to_string());
        }
    }

    if cands.len() == 2 && cands[0] == cands[1] {
        cands.pop();
    }
    return cands;
}

fn robots(path: &str, mut buttons: &mut String) -> Vec<String> {
    if path.len() <= 1 {
        return vec![buttons.to_string()];
    }
    let from_b = path.as_bytes()[0];
    let to_b = path.as_bytes()[1];
    let cands = get_cands(false, from_b as char, to_b as char);
    let mut ret = Vec::new();
    for cand in cands {
        let old_len = buttons.len();
        buttons.push_str(&cand);
        ret.extend(robots(&path[1..], &mut buttons));
        buttons.truncate(old_len);
    }
    
    ret
}

fn get_ans(maybes: &Vec<String>, code: &str) -> (String, i64) {
    let mini = maybes.iter()
        .min_by_key(|s| (s.len(), *s))
        .expect("maybes cannot be empty");

    let code_val = code[..code.len() - 1].parse::<i64>()
        .expect("Invalid code format");

    (mini.to_string(), code_val)
}



fn main() {
    let mut ans1 = 0;
    for line in fs::read_to_string("input").unwrap().lines() {
        let mut possible_paths = vec!["".to_string()];
        for (from_b, to_b) in "A".chars().chain(line.chars()).zip(line.chars()) {
            let cands = get_cands(true, from_b, to_b);
            let mut possible_paths_tmp = Vec::<String>::new();
            for cand in cands {
                for possible_path in &possible_paths {
                    possible_paths_tmp.push(format!("{}{}", possible_path, cand));
                }
            }
            possible_paths = possible_paths_tmp;
        }

        dbg!(&possible_paths);
        let mut maybe = possible_paths.clone();
        for i in 0..25 {
            println!("{} {}", i, maybe.len());
            let mut new_maybe = Vec::<String>::new();
            let mut mini: (String, i64) = ("".to_string(), 0);
            for a in &maybe {
                let maybe2 = robots(&format!("{}{}", 'A', a), &mut "".to_string());
                let mini_cand = get_ans(&maybe2, line);
                new_maybe.extend(maybe2);
                if mini.1 == 0 || mini_cand < mini {
                    mini = mini_cand;
                }
            }
            maybe = new_maybe;
            if i == 24 {
                ans1 += mini.0.len() as i64 * mini.1;
            }
        }
    }

    println!("ans {}", ans1);
}
