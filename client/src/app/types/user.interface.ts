export interface IAuthUser {
    username: string
    password: string
}

export interface ICreateUser {
    username: string
    profile_picture: string
    first_name: string
    last_name: string
    password_hash: string
    public_key: string
    enc_private_key: string
}

export interface IUser {
    username: string
    password_hash: string
    token: string
}

export interface ITokenInfo {
    access_token: string;
    token_type: string;
  }
