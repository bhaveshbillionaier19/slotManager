export type User = {
  id: string
  email: string
  name: string
}

export enum EventStatus {
  BUSY = 'BUSY',
  SWAPPABLE = 'SWAPPABLE',
  SWAP_PENDING = 'SWAP_PENDING',
}

export type Event = {
  id: string
  title: string
  start_time: string
  end_time: string
  status: EventStatus
}

export type TokenPayload = {
  user_id: string
  exp: number
}

export interface SwappableEventResponse extends Event {
  owner_name: string
}

export interface SwapRequestCreate {
  my_slot_id: string
  their_slot_id: string
}

export enum SwapRequestStatus {
  PENDING = 'PENDING',
  ACCEPTED = 'ACCEPTED',
  REJECTED = 'REJECTED',
}

export interface SwapRequestResponse {
  id: string
  requester_id: string
  offered_event_id: string
  requested_event_id: string
  status: SwapRequestStatus
  created_at: string
  updated_at: string
  offered_event_details?: Event
  requested_event_details?: Event
  requester_details?: User
}


