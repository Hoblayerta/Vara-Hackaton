// services.rs
// Necessary crates
use sails_rs::{prelude::*, gstd::msg};
use crate::states::state::*;

// Define the Service struct
#[derive(Default)]
pub struct Service;

// Implement functions for Service
impl Service {
    // Function to initialize the service state (call only once)
    pub fn seed() {
        State::init_state();
    }
}

#[service]
impl Service {
    // Constructor for Service
    pub fn new() -> Self {
        Self
    }

    // Service to register a new entry
    pub fn register_entry(&mut self, user: ActorId, description: String, number1: u32, number2: u32) -> Events {
        let state = State::state_mut();
        
        // Validations
        assert!(description.len() > 0, "Description cannot be empty.");
        assert!(number1 > 0 && number2 > 0, "Numbers must be positive.");

        // Register the entry
        state.register_entry(user, description, number1, number2);

        // Emit an event
        Events::EntryRegistered(user)
    }

    // Service to handle receive of data
    pub fn handle_receive(&mut self, user: ActorId, description: String, number1: u32, number2: u32) -> Events {
        // Add validation logic if required
        
        // Call the handler function
        State::state_mut().handle_receive(user, description, number1, number2);

        // Emit an event
        Events::Received(user)
    }

    // Service to handle request for user data
    pub fn handle_request_data(&self, user: ActorId) -> Option<(String, u32, u32)> {
        State::state_ref().handle_request_data(user)
    }

    // Queries
    pub fn query_get_all_users(&self) -> Vec<(ActorId, String)> {
        State::state_ref().all_users.clone()
    }

    pub fn query_get_registered_entries(&self) -> Vec<CustomStruct> {
        State::state_ref().register.iter().map(|(_, entry)| entry.clone()).collect()
    }

    pub fn query_get_admins(&self) -> Vec<ActorId> {
        State::state_ref().admins.clone()
    }
}

// Struct to use as a response to the user
#[derive(Encode, Decode, TypeInfo)]
#[codec(crate = sails_rs::scale_codec)]
#[scale_info(crate = sails_rs::scale_info)]
pub enum Events {
    EntryRegistered(ActorId),
    Received(ActorId),
}

