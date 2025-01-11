import { HexString } from '@gear-js/api';

interface ContractSails {
  programId: HexString,
  idl: string
}

export const ACCOUNT_ID_LOCAL_STORAGE_KEY = 'account';

export const ADDRESS = {
  NODE: import.meta.env.VITE_NODE_ADDRESS,
  BACK: import.meta.env.VITE_BACKEND_ADDRESS,
  GAME: import.meta.env.VITE_CONTRACT_ADDRESS as HexString,
};

export const ROUTES = {
  HOME: '/',
  EXAMPLES: '/examples',
  NOTFOUND: '*',
};

// To use the example code, enter the details of the account that will pay the vouchers, etc. (name and mnemonic)
// Here, you have an example account that contains tokens, in your dApp, you need to put a sponsor name
// and a sponsor mnemonic
export const sponsorName = 'Alice';
export const sponsorMnemonic = 'bottom drive obey lake curtain smoke basket hold race lonely fit walk';

export const CONTRACT_DATA: ContractSails = {
  programId: '0x9f770a55b154b373dcc1c8ffac49f12ce7ec0071fe5f029a74d479104ce5aa48',
  idl: `
    type Events = enum {
  EntryRegistered: actor_id,
  Received: actor_id,
};

type CustomStruct = struct {
  user: actor_id,
  description: str,
  number1: u32,
  number2: u32,
};

constructor {
  New : ();
};

service Service {
  HandleReceive : (user: actor_id, description: str, number1: u32, number2: u32) -> Events;
  RegisterEntry : (user: actor_id, description: str, number1: u32, number2: u32) -> Events;
  query HandleRequestData : (user: actor_id) -> opt struct { str, u32, u32 };
  query QueryGetAdmins : () -> vec actor_id;
  query QueryGetAllUsers : () -> vec struct { actor_id, str };
  query QueryGetRegisteredEntries : () -> vec CustomStruct;
};
  `
};