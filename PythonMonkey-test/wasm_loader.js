globalThis.crypto = {
    getRandomValues: (buf) => {
        if (
            !(buf instanceof Uint8Array || buf instanceof Int8Array ||
                buf instanceof Uint16Array || buf instanceof Int16Array ||
                buf instanceof Uint32Array || buf instanceof Int32Array)
        ) {
            throw new TypeError('Expected an integer TypedArray');
        }

        for (let i = 0; i < buf.length; i++) {
            buf[i] = Math.floor(Math.random() * 256);
        }

        return buf;
    }
}

// 设置全局 document 和 window（模拟浏览器环境）
global.window = globalThis
global.document = {
    querySelector: (selector) => {
        return createFakeElement(selector);
    },
};


global.window.navigator = {
    'webdriver': false
}

Object.defineProperty(global.window.navigator, 'webdriver', {
    get() {
        return false;
    },
    set(_) {
        // console.log('[navigator] attempt to modify "webdriver" ignored');
    }
});

function createFakeElement(selector = '') {
    const fakeElement = {

        getAttribute: (name) => {
            if (selector === "link[rel*='icon']") return "https://js-assets.mihuashi.com/favicon.ico"
            return null;
        },

        content: '米画师,mihuashi,约稿平台,约稿,插画外包,插画外包网站,美术外包平台,游戏美术外包,画师,绘师,美术外包,原画外包,插画师,原画师,原画外包网站'

    };


    return fakeElement;
}

var te = t => {
        throw TypeError(t)
    }
;
var $ = (t, e, n) => e.has(t) || te("Cannot " + n);
var o = (t, e, n) => ($(t, e, "read from private field"),
        n ? n.call(t) : e.get(t))
    ,
    A = (t, e, n) => e.has(t) ? te("Cannot add the same private member more than once") : e instanceof WeakSet ? e.add(t) : e.set(t, n)
    , v = (t, e, n, r) => ($(t, e, "write to private field"),
        r ? r.call(t, n) : e.set(t, n),
        n)
    , d = (t, e, n) => ($(t, e, "access private method"),
        n);

let _;
const p = new Array(128).fill(void 0);
p.push(void 0, null, !0, !1);

function i(t) {
    return p[t]
}

let L = p.length;

function l(t) {
    L === p.length && p.push(p.length + 1);
    const e = L;
    return L = p[e],
        p[e] = t,
        e
}

function S(t, e) {
    try {
        return t.apply(this, e)
    } catch (n) {
        _.__wbindgen_export_0(l(n))
    }
}

function T(t) {
    return t == null
}

const ie = typeof TextDecoder < "u" ? new TextDecoder("utf-8", {
    ignoreBOM: !0,
    fatal: !0
}) : {
    decode: () => {
        throw Error("TextDecoder not available")
    }
};
typeof TextDecoder < "u" && ie.decode();
let W = null;

function N() {
    return (W === null || W.byteLength === 0) && (W = new Uint8Array(_.memory.buffer)),
        W
}

function D(t, e) {
    return t = t >>> 0,
        ie.decode(N().subarray(t, t + e))
}

let C = 0;
const U = typeof TextEncoder < "u" ? new TextEncoder("utf-8") : {
        encode: () => {
            throw Error("TextEncoder not available")
        }
    }
    , he = typeof U.encodeInto == "function" ? function (t, e) {
            return U.encodeInto(t, e)
        }
        : function (t, e) {
            const n = U.encode(t);
            return e.set(n),
                {
                    read: t.length,
                    written: n.length
                }
        }
;

function B(t, e, n) {
    if (n === void 0) {
        const f = U.encode(t)
            , b = e(f.length, 1) >>> 0;
        return N().subarray(b, b + f.length).set(f),
            C = f.length,
            b
    }
    let r = t.length
        , s = e(r, 1) >>> 0;
    const c = N();
    let a = 0;
    for (; a < r; a++) {
        const f = t.charCodeAt(a);
        if (f > 127)
            break;
        c[s + a] = f
    }
    if (a !== r) {
        a !== 0 && (t = t.slice(a)),
            s = n(s, r, r = a + t.length * 3, 1) >>> 0;
        const f = N().subarray(s + a, s + r)
            , b = he(t, f);
        a += b.written,
            s = n(s, r, a, 1) >>> 0
    }
    return C = a,
        s
}

let E = null;

function m() {
    return (E === null || E.buffer.detached === !0 || E.buffer.detached === void 0 && E.buffer !== _.memory.buffer) && (E = new DataView(_.memory.buffer)),
        E
}

function me(t) {
    t < 132 || (p[t] = L,
        L = t)
}

function P(t) {
    const e = i(t);
    return me(t),
        e
}

function G(t) {
    const e = typeof t;
    if (e == "number" || e == "boolean" || t == null)
        return "".concat(t);
    if (e == "string")
        return '"'.concat(t, '"');
    if (e == "symbol") {
        const s = t.description;
        return s == null ? "Symbol" : "Symbol(".concat(s, ")")
    }
    if (e == "function") {
        const s = t.name;
        return typeof s == "string" && s.length > 0 ? "Function(".concat(s, ")") : "Function"
    }
    if (Array.isArray(t)) {
        const s = t.length;
        let c = "[";
        s > 0 && (c += G(t[0]));
        for (let a = 1; a < s; a++)
            c += ", " + G(t[a]);
        return c += "]",
            c
    }
    const n = /\[object ([^\]]+)\]/.exec(toString.call(t));
    let r;
    if (n && n.length > 1)
        r = n[1];
    else
        return toString.call(t);
    if (r == "Object")
        try {
            return "Object(" + JSON.stringify(t) + ")"
        } catch (s) {
            return "Object"
        }
    return t instanceof Error ? "".concat(t.name, ": ").concat(t.message, "\n").concat(t.stack) : r
}

const ne = typeof FinalizationRegistry > "u" ? {
    register: () => {
    }
    ,
    unregister: () => {
    }
} : new FinalizationRegistry(t => _.__wbg_signtool_free(t >>> 0, 1));

class pe {
    __destroy_into_raw() {
        const e = this.__wbg_ptr;
        return this.__wbg_ptr = 0,
            ne.unregister(this),
            e
    }

    free() {
        const e = this.__destroy_into_raw();
        _.__wbg_signtool_free(e, 0)
    }

    constructor() {
        const e = _.signtool_new();
        return this.__wbg_ptr = e >>> 0,
            ne.register(this, this.__wbg_ptr, this),
            this
    }

    sign(e, n) {
        let r, s;
        try {
            const y = _.__wbindgen_add_to_stack_pointer(-16)
                , fe = B(e, _.__wbindgen_export_1, _.__wbindgen_export_2)
                , le = C;
            _.signtool_sign(y, this.__wbg_ptr, fe, le, n);
            var c = m().getInt32(y + 4 * 0, !0)
                , a = m().getInt32(y + 4 * 1, !0)
                , f = m().getInt32(y + 4 * 2, !0)
                , b = m().getInt32(y + 4 * 3, !0)
                , x = c
                , O = a;
            if (b)
                throw x = 0,
                    O = 0,
                    P(f);
            return r = x,
                s = O,
                D(x, O)
        } finally {
            _.__wbindgen_add_to_stack_pointer(16),
                _.__wbindgen_export_3(r, s, 1)
        }
    }
}

async function ye(t, e) {


    const wasmModule = new WebAssembly.Module(t);
    const n = new WebAssembly.Instance(wasmModule, e);

    return n instanceof WebAssembly.Instance ? {
        instance: n,
        module: t
    } : n

}

function Se() {
    const t = {};
    return t.wbg = {},
        t.wbg.__wbg_buffer_609cc3eee51ed158 = function (e) {
            const n = i(e).buffer;
            return l(n)
        }
        ,
        t.wbg.__wbg_call_672a4d21634d4a24 = function () {
            return S(function (e, n) {
                const r = i(e).call(i(n));
                return l(r)
            }, arguments)
        }
        ,
        t.wbg.__wbg_call_7cccdd69e0791ae2 = function () {
            return S(function (e, n, r) {
                const s = i(e).call(i(n), i(r));
                return l(s)
            }, arguments)
        }
        ,
        t.wbg.__wbg_crypto_ed58b8e10a292839 = function (e) {
            const n = i(e).crypto;
            return l(n)
        }
        ,
        t.wbg.__wbg_document_d249400bd7bd996d = function (e) {
            const n = i(e).document;
            return T(n) ? 0 : l(n)
        }
        ,
        t.wbg.__wbg_getAttribute_ea5166be2deba45e = function (e, n, r, s) {
            const c = i(n).getAttribute(D(r, s));
            var a = T(c) ? 0 : B(c, _.__wbindgen_export_1, _.__wbindgen_export_2)
                , f = C;
            m().setInt32(e + 4 * 1, f, !0),
                m().setInt32(e + 4 * 0, a, !0)
        }
        ,
        t.wbg.__wbg_getRandomValues_bcb4912f16000dc4 = function () {
            return S(function (e, n) {
                i(e).getRandomValues(i(n))
            }, arguments)
        }
        ,
        t.wbg.__wbg_get_67b2ba62fc30de12 = function () {
            return S(function (e, n) {
                const r = Reflect.get(i(e), i(n));
                return l(r)
            }, arguments)
        }
        ,
        t.wbg.__wbg_instanceof_Window_def73ea0955fc569 = function (e) {
            let n;
            try {
                n = i(e) === global.window
            } catch (s) {
                n = !1
            }
            return n
        }
        ,
        t.wbg.__wbg_msCrypto_0a36e2ec3a343d26 = function (e) {
            const n = i(e).msCrypto;
            return l(n)
        }
        ,
        t.wbg.__wbg_navigator_1577371c070c8947 = function (e) {
            const n = i(e).navigator;
            return l(n)
        }
        ,
        t.wbg.__wbg_new_a12002a7f91c75be = function (e) {
            const n = new Uint8Array(i(e));
            return l(n)
        }
        ,
        t.wbg.__wbg_newnoargs_105ed471475aaf50 = function (e, n) {
            const r = new Function(D(e, n));
            return l(r)
        }
        ,
        t.wbg.__wbg_newwithbyteoffsetandlength_d97e637ebe145a9a = function (e, n, r) {
            const s = new Uint8Array(i(e), n >>> 0, r >>> 0);
            return l(s)
        }
        ,
        t.wbg.__wbg_newwithlength_a381634e90c276d4 = function (e) {
            const n = new Uint8Array(e >>> 0);
            return l(n)
        }
        ,
        t.wbg.__wbg_node_02999533c4ea02e3 = function (e) {
            const n = i(e).node;
            return l(n)
        }
        ,
        t.wbg.__wbg_process_5c1d670bc53614b8 = function (e) {
            const n = i(e).process;
            return l(n)
        }
        ,
        t.wbg.__wbg_querySelector_c69f8b573958906b = function () {
            return S(function (e, n, r) {
                // console.log(D(n, r))
                const s = i(e).querySelector(D(n, r));
                return T(s) ? 0 : l(s)
            }, arguments)
        }
        ,
        t.wbg.__wbg_randomFillSync_ab2cfe79ebbf2740 = function () {
            return S(function (e, n) {
                i(e).randomFillSync(P(n))
            }, arguments)
        }
        ,
        t.wbg.__wbg_require_79b1e9274cde3c87 = function () {
            return S(function () {
                const e = module.require;
                return l(e)
            }, arguments)
        }
        ,
        t.wbg.__wbg_set_65595bdd868b3009 = function (e, n, r) {
            i(e).set(i(n), r >>> 0)
        }
        ,
        t.wbg.__wbg_set_bb8cecf6a62b9f46 = function () {
            return S(function (e, n, r) {
                return Reflect.set(i(e), i(n), i(r))
            }, arguments)
        }
        ,
        t.wbg.__wbg_static_accessor_GLOBAL_88a902d13a557d07 = function () {
            const e = typeof global > "u" ? null : global;
            return T(e) ? 0 : l(e)
        }
        ,
        t.wbg.__wbg_static_accessor_GLOBAL_THIS_56578be7e9f832b0 = function () {
            const e = typeof globalThis > "u" ? null : globalThis;
            return T(e) ? 0 : l(e)
        }
        ,
        t.wbg.__wbg_static_accessor_PROCESS_2c90d3b3264f2c90 = function () {
            const e = process;
            return l(e)
        }
        ,
        t.wbg.__wbg_static_accessor_SELF_37c5d418e4bf5819 = function () {
            const e = typeof global.window > "u" ? null : global.window;
            return T(e) ? 0 : l(e)
        }
        ,
        t.wbg.__wbg_static_accessor_WINDOW_5de37043a91a9c40 = function () {
            const e = typeof window > "u" ? null : window;
            return T(e) ? 0 : l(e)
        }
        ,
        t.wbg.__wbg_subarray_aa9065fa9dc5df96 = function (e, n, r) {
            const s = i(e).subarray(n >>> 0, r >>> 0);
            return l(s)
        }
        ,
        t.wbg.__wbg_versions_c71aa1626a93e0a1 = function (e) {
            const n = i(e).versions;
            return l(n)
        }
        ,
        t.wbg.__wbindgen_boolean_get = function (e) {
            const n = i(e);
            return typeof n == "boolean" ? n ? 1 : 0 : 2
        }
        ,
        t.wbg.__wbindgen_debug_string = function (e, n) {
            const r = G(i(n))
                , s = B(r, _.__wbindgen_export_1, _.__wbindgen_export_2)
                , c = C;
            m().setInt32(e + 4 * 1, c, !0),
                m().setInt32(e + 4 * 0, s, !0)
        }
        ,
        t.wbg.__wbindgen_is_function = function (e) {
            if (i(e) && (i(e).name === 'abort' || i(e).name === 'exit')) return false;
            return typeof i(e) == "function"
        }
        ,
        t.wbg.__wbindgen_is_object = function (e) {
            const n = i(e);
            return typeof n == "object" && n !== null
        }
        ,
        t.wbg.__wbindgen_is_string = function (e) {
            return typeof i(e) == "string"
        }
        ,
        t.wbg.__wbindgen_is_undefined = function (e) {
            return i(e) === void 0
        }
        ,
        t.wbg.__wbindgen_memory = function () {
            const e = _.memory;
            console.log(e)
            return l(e)
        }
        ,
        t.wbg.__wbindgen_number_new = function (e) {
            return l(e)
        }
        ,
        t.wbg.__wbindgen_object_clone_ref = function (e) {
            const n = i(e);
            return l(n)
        }
        ,
        t.wbg.__wbindgen_object_drop_ref = function (e) {
            P(e)
        }
        ,
        t.wbg.__wbindgen_string_get = function (e, n) {
            const r = i(n)
                , s = typeof r == "string" ? r : void 0;
            var c = T(s) ? 0 : B(s, _.__wbindgen_export_1, _.__wbindgen_export_2)
                , a = C;

            m().setInt32(e + 4 * 1, a, !0),
                m().setInt32(e + 4 * 0, c, !0)
        }
        ,
        t.wbg.__wbindgen_string_new = function (e, n) {
            const r = D(e, n);
            return l(r)
        }
        ,
        t.wbg.__wbindgen_throw = function (e, n) {
            throw new Error(D(e, n))
        }
        ,
        t
}

function Te(t, e) {
    return _ = t.exports,
        ce.__wbindgen_wasm_module = e,
        E = null,
        W = null,
        _
}

async function ce(t) {

    // 读取 WebAssembly 文件
    const wasmPath = "./mhs_sign.wasm"
    const wasmBuffer = readFileSync(wasmPath);
    const e = Se();

    // 假设 t.wbg 已经存在并包含若干函数
    for (const key in e.wbg) {
        if (typeof e.wbg[key] === 'function') {
            const originalFunc = e.wbg[key];

            e.wbg[key] = function (...args) {
                console.log(`[Input] ${key}:`, ...args);
                try {
                    const result = originalFunc.apply(this, args);
                    // 如果返回的是 Promise，也跟踪它的结果
                    if (result instanceof Promise) {
                        return result.then(res => {
                            console.log(`[Output] ${key}:`, res);
                            return res;
                        }).catch(err => {
                            console.log(`[Error] ${key}:`, err);
                            throw err;
                        });
                    } else {
                        console.log(`[Output] ${key}:`, result);
                        return result;
                    }
                } catch (err) {
                    console.log(`[Error] ${key}:`, err);
                    throw err;
                }
            };
        }
    }


    const {instance: n, module: r} = await ye(wasmBuffer, e);
    return Te(n, r)
}

const xe = "https://js-assets.mihuashi.com/assets/mhs_fe_sign_bg.BRq86mik.wasm";
let z;
const Ie = async () => ce(xe)
    , Ee = () => {
    if (!z)
        try {
            z = new pe
        } catch (t) {
            console.error("signTool init failed")
        }
    return z
}
    , Ue = Ie()
    , ee = {
    log: (...t) => {
        window.__MHS_LOG_TIME_SYNC__ != null && console.log("[TimeSync]:", ...t)
    }
    ,
    table: t => {
        window.__MHS_LOG_TIME_SYNC__ != null && console.table({
            scope: "[TIME_SYNC]",
            ...t
        })
    }
};
var g, h, j, R, u, w, Y, M, F, Z, ue, J, K;

class Oe {
    constructor(e) {
        A(this, u);
        A(this, g, []);
        A(this, h);
        A(this, j);
        A(this, R);
        v(this, h, e.sampleCount),
            v(this, j, e.maxStandardDeviation),
            v(this, R, e.outlierThreshold)
    }

    reset() {
        v(this, g, [])
    }

    getSample(e) {
        return d(this, u, K).call(this, {
            name: "before get(add)Sample",
            sample: e
        }),
            e == null ? o(this, u, w) : d(this, u, J).call(this, e) ? (o(this, g).push(e),
            o(this, g).length > o(this, h) && d(this, u, ue).call(this),
                d(this, u, K).call(this, {
                    name: "after get(add)Sample",
                    sample: e
                }),
                o(this, u, w)) : o(this, u, w)
    }

    get isReliable() {
        const e = o(this, g).length >= o(this, h);
        if (o(this, u, M) == null)
            return !1;
        const n = o(this, u, M) <= o(this, j);
        return e && n
    }
}

g = new WeakMap,
    h = new WeakMap,
    j = new WeakMap,
    R = new WeakMap,
    u = new WeakSet,
    w = function () {
        return o(this, g).length === 0 ? null : o(this, g).reduce((n, r) => n + r, 0) / o(this, g).length
    }
    ,
    Y = function () {
        if (o(this, u, w) == null || o(this, g).length < 2)
            return null;
        const e = o(this, u, w);
        return o(this, g).reduce((n, r) => n + (r - e) ** 2, 0) / o(this, g).length
    }
    ,
    M = function () {
        return o(this, u, Y) == null ? null : Math.sqrt(o(this, u, Y))
    }
    ,
    F = function (e) {
        if (o(this, u, w) == null || o(this, u, M) == null)
            return null;
        const n = o(this, u, M);
        return n === 0 ? 0 : Math.abs(e - o(this, u, w)) / n
    }
    ,
    Z = function (e) {
        if (o(this, g).length < o(this, h))
            return !1;
        const n = d(this, u, F).call(this, e);
        return n == null ? !1 : n > o(this, R)
    }
    ,
    ue = function () {
        if (o(this, g).length < o(this, h))
            return;
        let e = 0
            , n = -1;
        o(this, g).forEach((r, s) => {
                const c = d(this, u, F).call(this, r);
                c != null && c > e && (e = c,
                    n = s)
            }
        ),
        n != -1 && o(this, g).splice(n, 1)
    }
    ,
    J = function (e) {
        return o(this, u, w) == null || o(this, g).length < o(this, h) ? !0 : !d(this, u, Z).call(this, e)
    }
    ,
    K = function ({sample: e, name: n}) {
        ee.table({
            name: n,
            sample: e,
            average: o(this, u, w),
            standardDeviation: o(this, u, M),
            outlierThreshold: o(this, R),
            zScore: e != null ? d(this, u, F).call(this, e) : 0,
            isOutlier: e != null ? d(this, u, Z).call(this, e) : !1,
            samples: o(this, g),
            isReliable: this.isReliable,
            sampleCount: o(this, h),
            maxStandardDeviation: o(this, j),
            isSampleValid: e != null ? d(this, u, J).call(this, e) : !1
        })
    }
;
const ae = 1e3
    , re = t => Math.floor(t / 1e3)
    , V = new Oe({
    sampleCount: 5,
    maxStandardDeviation: 500,
    outlierThreshold: 2
});
let Q = null
    , X = null;
const Ae = t => {
    Q != null && t.http.interceptors.request.eject(Q),
    X != null && t.http.interceptors.response.eject(X)
}
    , De = t => (Object.assign(t, {
    context: {
        time: Date.now()
    }
}),
    t);
let H = !1;
const se = (t, e) => {
        var x, O, y;
        if (H)
            return;
        H = !0;
        const n = () => (H = !1,
                t)
            ,
            r = t.headers && typeof t.headers.get == "function" ? (x = t.headers.get("date")) == null ? void 0 : x.toString() : void 0
            , s = t.headers && typeof t.headers.get == "function" ? t.headers.get("cache-control", !0) : void 0
            , c = () => s != null && typeof s == "object" && "max-age" in s ? Number.parseInt(s["max-age"]) > ae : !1;
        if (ee.table({
            name: "cache-control in response",
            cacheControl: s
        }),
        !r || c())
            return n();
        const a = de(r).toDate().getTime()
            , f = (y = (O = t.config) == null ? void 0 : O.context) == null ? void 0 : y.time;
        if (f == null)
            return n();
        const {done: b} = Ce({
            serverTime: a,
            requestTime: f
        });
        return b && Ae(e),
            n()
    }
    , Me = t => {
        Q = t.http.interceptors.request.use(e => (De(e),
            e), e => (console.error("request error", e),
            Promise.reject(e))),
            X = t.http.interceptors.response.use(e => (se(e, t),
                e), e => (e instanceof we && e.response && se(e.response, t),
                console.error("response error", e),
                Promise.reject(e)))
    }
;

function Ce(t) {
    const e = oe();
    if (typeof e.wsNow == "number")
        return {
            done: !0
        };
    const n = Date.now()
        , r = n - t.requestTime
        , s = r / 2
        , c = t.serverTime + s
        , a = c - n;
    if (Math.abs(r) > 3e3)
        return {
            done: !1
        };
    const f = V.getSample(a);
    return f && V.isReliable ? (e.offset !== 0 && (e.offset = re(f)),
        ee.table({
            name: "offset is reliable and set to userStore.offset",
            requestDuration: r,
            networkDelay: s,
            adjustedServerTime: c,
            diff: a,
            now: n,
            time: t,
            "userStore.offset": e.offset
        }),
        V.reset(),
        {
            done: !0
        }) : (f != null && (Math.abs(f) > ae || e.offset !== 0) && (e.offset = re(f)),
        {
            done: !1
        })
}


async function init() {
    await Ie();
    const s = await Ee();
    console.log(s.sign("/api/v1/artworks/search", "1752327668"))
}

init()

module.exports = {Ie, Ee};