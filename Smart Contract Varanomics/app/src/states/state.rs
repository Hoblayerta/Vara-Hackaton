// State.rs
// Necesary crates
use sails_rs::{
    prelude::*,
};

// Static mutable variable (contract's state)
pub static mut STATE: Option<State> = None;

// Create a struct for the state
#[derive(Clone, Default)]
pub struct State {
    pub admins: Vec<ActorId>,
    pub all_users: Vec<(ActorId, String)>,
    pub register: Vec<(ActorId, CustomStruct)>,
}

// Struct para representar una denuncia
#[derive(Encode, Decode, TypeInfo, Clone)]
#[codec(crate = sails_rs::scale_codec)]
#[scale_info(crate = sails_rs::scale_info)]
pub struct CustomStruct {
    pub user: ActorId,
    pub description: String,
    pub number1: u32,
    pub number2: u32,
}

// Impl to set methods or related functions
impl State {
    // Method to create a new instance
    pub fn new() -> Self {
        Self { ..Default::default() }
    }

    // Related function to init the state
    pub fn init_state() {
        unsafe {
            STATE = Some(Self::new());
        };
    }

    // Related function to get the state as mut
    pub fn state_mut() -> &'static mut State {
        let state = unsafe { STATE.as_mut() };
        debug_assert!(state.is_some(), "The state is not initialized");
        unsafe { state.unwrap_unchecked() }
    }

    // Related function to get the state as ref
    pub fn state_ref() -> &'static State {
        let state = unsafe { STATE.as_ref() };
        debug_assert!(state.is_some(), "The state is not initialized");
        unsafe { state.unwrap_unchecked() }
    }

    // Function to register a new entry
    pub fn register_entry(&mut self, user: ActorId, description: String, number1: u32, number2: u32) {
        let new_entry = CustomStruct {
            user,
            description,
            number1,
            number2,
        };
        self.register.push((user, new_entry));
    }

    // Function to get data for a user
    pub fn get_user_data(&self, user: &ActorId) -> Option<&CustomStruct> {
        self.register.iter().find_map(|(u, entry)| {
            if u == user {
                Some(entry)
            } else {
                None
            }
        })
    }
}

// Create a struct that can be sent to the user who reads the state
#[derive(Encode, Decode, TypeInfo)]
#[codec(crate = sails_rs::scale_codec)]
#[scale_info(crate = sails_rs::scale_info)]
pub struct IoState {
    pub admins: Vec<ActorId>,
    pub all_users: Vec<(ActorId, String)>,
    pub register: Vec<CustomStruct>,
}

#[derive(Debug, Decode, Encode, TypeInfo)]
#[codec(crate = gstd::codec)]
#[scale_info(crate = gstd::scale_info)]
pub enum Errors {}

impl From<State> for IoState {
    fn from(value: State) -> Self {
        let State {
            admins,
            all_users,
            register,
        } = value;

        Self {
            admins,
            all_users: all_users.clone(),
            register: register.iter().map(|(_, v)| v.clone()).collect(),
        }
    }
}

// Smart contract function implementations
impl State {
    // Handle receive text and numbers
    pub fn handle_receive(&mut self, user: ActorId, description: String, number1: u32, number2: u32) {
        self.register_entry(user, description, number1, number2);
    }

    // Handle request data
    pub fn handle_request_data(&self, user: ActorId) -> Option<(String, u32, u32)> {
        self.get_user_data(&user).map(|entry| {
            let CustomStruct {
                description,
                number1,
                number2,
                ..
            } = entry;
            (description.clone(), *number1, *number2)
        })
    }
}