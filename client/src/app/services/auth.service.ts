import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { Injectable, signal } from "@angular/core";
import { Router } from "@angular/router";
import { ToastrService } from "ngx-toastr";
import { IAuthUser, ICreateUser, ITokenInfo } from "../types/user.interface";
import { API_URL } from "../constants/constants";
import { catchError, tap } from "rxjs";
import * as bcrypt from 'bcryptjs';
import * as CryptoJS from 'crypto-js';
import * as forge from 'node-forge';
import { SHA256 } from 'crypto-js';

@Injectable({
    providedIn: "root",
})
export class AuthService {

    isAuthSig = signal<boolean>(false)

    constructor(
        private readonly http: HttpClient,
        private readonly router: Router,
        private readonly toastr: ToastrService,
    ){
        const token = localStorage.getItem('token')
        this.isAuthSig.set(!!token)
    }

    signUp(userData:IAuthUser){
        const { publicKey, privateKey } = forge.pki.rsa.generateKeyPair({ bits: 1024 });
        const publicKeyPem = forge.pki.publicKeyToPem(publicKey);
        const privateKeyPem = forge.pki.privateKeyToPem(privateKey);
        const iv = '1234567890123456';
        const ivWordArray = CryptoJS.enc.Hex.parse(iv);
        const privateKeyPem_Enc = CryptoJS.AES.encrypt(privateKeyPem,
             userData.password, { iv: ivWordArray }).toString();
        const userDataSend: ICreateUser = {
            username: userData.username,
            profile_picture: "",
            first_name: "testWEB",
            last_name: "testWEB",
            password_hash: SHA256(userData.password).toString(),
            public_key: publicKeyPem,
            enc_private_key: privateKeyPem_Enc
        };
        console.log("gen all")
        return this.http.post(`${API_URL}/api/v1/users/`, userDataSend)
        .pipe(
            tap(()=>{
                this.login(userData)
            }),
            catchError(err => {
                this.toastr.error("Username is already taken")
                throw new Error(err.message)
            })
        )
        .subscribe(
            ()=>{this.toastr.success('New account created succesfully')}
        )
    }

    private handleError(err: HttpErrorResponse): void {
        this.toastr.error("Invalid username or password")
    }

    login(userData: IAuthUser){
        const hashed_password =  SHA256(userData.password).toString()
        console.log(hashed_password)
        const formData = new FormData();
        formData.append('username', userData.username);
        formData.append('password', hashed_password);

        return this.http.post<ITokenInfo>(`${API_URL}/api/v1/jwt_auth/jwt/login/`, formData)
        .pipe(
            tap( (res: ITokenInfo) =>{
                localStorage.setItem('token', res.access_token)
                this.isAuthSig.set(true)
            }),
            catchError(err => {
                this.handleError(err)
                throw new Error(err.message)
            })
        )
        .subscribe(
            ()=>{
                this.toastr.success('Logged in succesfully')
                this.router.navigate(['/home'])
            }
        )
    }

    logout(){
        localStorage.removeItem('token')
        this.isAuthSig.set(false)
        this.router.navigate(['/login'])
        this.toastr.success('Logged out successfully')
    }
    
}